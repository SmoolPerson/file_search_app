"""FastAPI server for executing Griptape Nodes workflows."""

import importlib
import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from griptape_nodes.bootstrap.workflow_executors.local_workflow_executor import LocalWorkflowExecutor
from griptape_nodes.drivers.storage.storage_backend import StorageBackend
from griptape_nodes.retained_mode.events.flow_events import GetTopLevelFlowRequest, GetTopLevelFlowResultSuccess
from griptape_nodes.retained_mode.events.library_events import RegisterLibraryFromFileRequest
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get workflow module from environment variable
WORKFLOW_MODULE = f"workflows.{os.environ.get('WORKFLOW_MODULE', 'poem_flow')}"

# Global executor instance
_executor: LocalWorkflowExecutor | None = None
_executor_initialized = False


class WorkflowRequest(BaseModel):
    """Generic input model for workflow execution.

    The flow_input field contains the complete workflow input structure,
    including the "Start Flow" key and all workflow-specific parameters.
    """

    flow_input: dict[str, Any]


class WorkflowResponse(BaseModel):
    """Generic output model for workflow execution.

    The output field contains the complete workflow output structure,
    including the "End Flow" key and all workflow-specific outputs.
    """

    output: dict[str, Any] | None


def _ensure_workflow_context() -> None:
    """Ensure the workflow context is properly set up."""
    context_manager = GriptapeNodes.ContextManager()
    if context_manager.has_current_flow():
        return

    top_level_flow_request = GetTopLevelFlowRequest()
    top_level_flow_result = GriptapeNodes.handle_request(top_level_flow_request)
    if not isinstance(top_level_flow_result, GetTopLevelFlowResultSuccess):
        return
    if top_level_flow_result.flow_name is None:
        return

    flow_manager = GriptapeNodes.FlowManager()
    flow_obj = flow_manager.get_flow_by_name(top_level_flow_result.flow_name)
    context_manager.push_flow(flow_obj)


def _get_executor() -> LocalWorkflowExecutor:
    """Get or create the workflow executor instance."""
    global _executor  # noqa: PLW0603
    if _executor is None:
        storage_backend_enum = StorageBackend.LOCAL
        _executor = LocalWorkflowExecutor(storage_backend=storage_backend_enum)
    return _executor


def _register_local_libraries() -> None:
    """Register the project's local libraries with Griptape Nodes."""
    project_root = Path(__file__).parent

    # Define the libraries to register
    libraries_to_register = [
        project_root / "griptape_nodes_library" / "griptape_nodes_library.json",
        project_root / "griptape-nodes-library-neo4j" / "neo4j_nodes_library" / "griptape_nodes_library.json",
    ]

    for library_path in libraries_to_register:
        if library_path.exists():
            try:
                logger.info("Registering library: %s", library_path)
                result = GriptapeNodes.handle_request(
                    RegisterLibraryFromFileRequest(file_path=str(library_path.absolute()))
                )

                if hasattr(result, "was_successful") and result.was_successful:
                    logger.info("Successfully registered library: %s", library_path.name)
                else:
                    logger.warning(
                        "Failed to register library %s: %s",
                        library_path,
                        getattr(result, "result_details", "Unknown error"),
                    )

            except Exception:
                logger.exception("Error registering library: %s", library_path)
        else:
            logger.warning("Library not found: %s", library_path)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Lifespan context manager for FastAPI startup/shutdown."""
    # Register local libraries before loading the workflow
    logger.info("Registering local libraries...")
    _register_local_libraries()

    # Load the workflow module
    logger.info("Loading workflow module: %s", WORKFLOW_MODULE)
    print(f"Loading workflow module: {WORKFLOW_MODULE}")
    importlib.import_module(WORKFLOW_MODULE)
    logger.info("Workflow module %s loaded successfully", WORKFLOW_MODULE)
    yield


# FastAPI app with lifespan
app = FastAPI(title="Griptape Nodes Workflow Server", lifespan=lifespan)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "workflow_module": WORKFLOW_MODULE}


@app.post("/run")
async def run_workflow(request: WorkflowRequest) -> WorkflowResponse:
    """Execute the workflow with the given flow_input.

    The flow_input should contain the complete workflow input structure,
    typically with a "Start Flow" key containing all workflow parameters.

    Returns the raw workflow output dict.
    """
    global _executor_initialized  # noqa: PLW0603

    try:
        executor = _get_executor()
        _ensure_workflow_context()

        if not _executor_initialized:
            await executor.__aenter__()
            _executor_initialized = True

        await executor.arun(flow_input=request.flow_input, pickle_control_flow_result=False)
        output = json.loads(json.dumps(executor.output))  # Deep copy to avoid serialization issues

        return WorkflowResponse(output=output)

    except Exception as e:
        logger.exception("Workflow execution failed")
        return WorkflowResponse(output={"error": str(e)})
