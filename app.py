import streamlit as st
from workflow_server_manager import WorkflowServerManager
import httpx
import asyncio
import json

def main():
    st.set_page_config(page_title="AI Graph Search", layout="wide")
    info_markdown = """
        # 🔍 AI Graph Search

        A lightweight, AI-powered search engine built on top of a graph database.  
        The system uses intelligent graph traversal—guided by sophisticated LLM ranking—to quickly surface the most relevant nodes and relationships.

        **Key points:**
        - Graph-backed data model for rich connections  
        - Fast, AI-assisted traversal for rapid, relevant search results  
        - Designed for flexible, semantic querying over complex datasets"""

    tab1, tab2, tab3 = st.tabs(["Info", "Index Directories", "Search"])
    with tab1:
        st.markdown(info_markdown)
    with tab2:
        st.header("Index Directories")
        st.write("Click the button to index a specific directory! Put the directory path in the text box below!")
        st.write("Note: Indexing may take some time depending on the size of the directory.")
        dir_path = st.text_input("Directory Path", "/path/to/directory")
        if st.button("Index Directory"):
            st.write(f"Indexing directory: {dir_path}")
            # Placeholder for indexing logic
            output = asyncio.run(execute_workflow_async(dir_path, "workflow_recreation"))
            st.write(f"Indexing complete!")
    with tab3:
        st.header("Search")
        st.write("Select the indexed directory you would like to search from the dropdown below!")
        option = st.selectbox(
            "What directory would you like to search?",
            ("/random", "/images", "/arbitrary"),
        )
        st.write("Tell us what you want to search!")
        query = st.text_input("Search query", "Find all files with cats?")
        if st.button("Search"):
            st.write(f"Searching in directory: {option}")
            # Placeholder for search logic
            output = asyncio.run(execute_workflow_async(query, "retrieval_v2"))
            st.write("Search complete! Displaying results...")
            st.write(output["agent_result"])

@st.cache_resource
def get_server_manager() -> WorkflowServerManager:
    """Get or create the workflow server manager."""
    return WorkflowServerManager.get_instance()


async def call_workflow_server(port: int, flow_input: dict) -> dict:
    """Call a workflow server's /run endpoint.

    Args:
        port: The port the workflow server is running on
        flow_input: The complete flow input dict (including "Start Flow" key)

    Returns:
        The workflow output dict from the server response
    """
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            f"http://localhost:{port}/run",
            json={"flow_input": flow_input},
        )
        response.raise_for_status()
        result = response.json()
        return result.get("output", {})

async def execute_workflow_async(  # noqa: PLR0913
    query: str, workflow_name: str
) -> dict:
    """Execute the Griptape Nodes workflow via HTTP.

    Args:
        sample_input: The sample input string to process

    Returns:
        str: Contains workflow output, which is the same input string but with 's' appended to it. 
    """
    flow_input = {
        "Start Flow": {
            "text": query,
        }
    }

    manager = get_server_manager()
    port = manager.get_port(workflow_name)

    if port is None:
        return {
            "was_successful": False,
            "result_details": "Workflow server not configured",
        }

    try:
        output = await call_workflow_server(port, flow_input)

        # Check for error in output
        if "error" in output:
            return {
                "was_successful": False,
                "result_details": f"Workflow error: {output['error']}",
            }

        # Parse the End Flow data from the raw output
        end_flow_data = output.get("End Flow", {})

        return {
            "was_successful": end_flow_data.get("was_successful", False),
            "agent_result": end_flow_data.get("text", ""),
        }
    except httpx.RequestError as e:
        return {
            "was_successful": False,
            "result_details": f"Failed to connect to workflow server: {e}",
        }
    except httpx.HTTPStatusError as e:
        return {
            "was_successful": False,
            "result_details": f"Workflow server error: {e.response.status_code}",
        }
    
if __name__ == "__main__":
    main()