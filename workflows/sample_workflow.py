# /// script
# dependencies = []
# 
# [tool.griptape-nodes]
# name = "sample_workflow"
# schema_version = "0.14.0"
# engine_version_created_with = "0.66.3"
# node_libraries_referenced = [["Griptape Nodes Library", "0.55.0"]]
# node_types_used = [["Griptape Nodes Library", "EndFlow"], ["Griptape Nodes Library", "MergeTexts"], ["Griptape Nodes Library", "StartFlow"]]
# is_griptape_provided = false
# creation_date = 2026-01-02T21:59:41.769182Z
# last_modified_date = 2026-01-02T23:36:15.248518Z
# workflow_shape = "{\"inputs\":{\"Start Flow\":{\"exec_out\":{\"name\":\"exec_out\",\"tooltip\":\"Connection to the next node in the execution chain\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Flow Out\"},\"settable\":true,\"is_user_defined\":true,\"private\":false,\"parent_container_name\":null,\"parent_element_name\":null},\"sample_input\":{\"name\":\"sample_input\",\"tooltip\":\"Enter text/string for sample_input.\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"is_custom\":true,\"is_user_added\":true},\"settable\":true,\"is_user_defined\":true,\"private\":false,\"parent_container_name\":null,\"parent_element_name\":null}}},\"outputs\":{\"End Flow\":{\"exec_in\":{\"name\":\"exec_in\",\"tooltip\":\"Control path when the flow completed successfully\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Succeeded\"},\"settable\":true,\"is_user_defined\":true,\"private\":false,\"parent_container_name\":null,\"parent_element_name\":null},\"failed\":{\"name\":\"failed\",\"tooltip\":\"Control path when the flow failed\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Failed\"},\"settable\":true,\"is_user_defined\":true,\"private\":false,\"parent_container_name\":null,\"parent_element_name\":null},\"was_successful\":{\"name\":\"was_successful\",\"tooltip\":\"Indicates whether it completed without errors.\",\"type\":\"bool\",\"input_types\":[\"bool\"],\"output_type\":\"bool\",\"default_value\":false,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{},\"settable\":false,\"is_user_defined\":true,\"private\":false,\"parent_container_name\":null,\"parent_element_name\":null},\"result_details\":{\"name\":\"result_details\",\"tooltip\":\"Details about the operation result\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"multiline\":true,\"placeholder_text\":\"Details about the completion or failure will be shown here.\"},\"settable\":false,\"is_user_defined\":true,\"private\":false,\"parent_container_name\":null,\"parent_element_name\":null},\"sample_output\":{\"name\":\"sample_output\",\"tooltip\":\"Enter text/string for sample_output.\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"is_custom\":true,\"is_user_added\":true},\"settable\":true,\"is_user_defined\":true,\"private\":false,\"parent_container_name\":null,\"parent_element_name\":null}}}}"
# 
# ///

import argparse
import asyncio
import json
import pickle
from griptape_nodes.bootstrap.workflow_executors.local_workflow_executor import LocalWorkflowExecutor
from griptape_nodes.bootstrap.workflow_executors.workflow_executor import WorkflowExecutor
from griptape_nodes.drivers.storage.storage_backend import StorageBackend
from griptape_nodes.node_library.library_registry import IconVariant, NodeDeprecationMetadata, NodeMetadata
from griptape_nodes.retained_mode.events.connection_events import CreateConnectionRequest
from griptape_nodes.retained_mode.events.flow_events import CreateFlowRequest, GetTopLevelFlowRequest, GetTopLevelFlowResultSuccess
from griptape_nodes.retained_mode.events.library_events import LoadLibrariesRequest
from griptape_nodes.retained_mode.events.node_events import CreateNodeRequest
from griptape_nodes.retained_mode.events.parameter_events import AddParameterToNodeRequest, AlterParameterDetailsRequest, SetParameterValueRequest
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

GriptapeNodes.handle_request(LoadLibrariesRequest())

context_manager = GriptapeNodes.ContextManager()

if not context_manager.has_current_workflow():
    context_manager.push_workflow(workflow_name='sample_workflow')

"""
1. We've collated all of the unique parameter values into a dictionary so that we do not have to duplicate them.
   This minimizes the size of the code, especially for large objects like serialized image files.
2. We're using a prefix so that it's clear which Flow these values are associated with.
3. The values are serialized using pickle, which is a binary format. This makes them harder to read, but makes
   them consistently save and load. It allows us to serialize complex objects like custom classes, which otherwise
   would be difficult to serialize.
"""
top_level_unique_values_dict = {'575ee2e2-1311-4e5c-9b36-c246fb10c037': pickle.loads(b'\x80\x04\x89.'), '3ce44a4a-7494-4025-854c-ae2b0907ea4f': pickle.loads(b'\x80\x04\x95\x05\x00\x00\x00\x00\x00\x00\x00\x8c\x01s\x94.'), 'b7057fc6-d824-4b9b-83d3-9a36a347a422': pickle.loads(b'\x80\x04\x95\x04\x00\x00\x00\x00\x00\x00\x00\x8c\x00\x94.')}

'# Create the Flow, then do work within it as context.'

flow0_name = GriptapeNodes.handle_request(CreateFlowRequest(parent_flow_name=None, flow_name='ControlFlow_1', set_as_new_context=False, metadata={})).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(CreateNodeRequest(node_type='EndFlow', specific_library_name='Griptape Nodes Library', node_name='End Flow', metadata={'position': {'x': 2767.955859083676, 'y': 176.21746908643777}, 'tempId': 'placing-1767391239354-dsq3m', 'library_node_metadata': NodeMetadata(category='workflows', description='Define the end of a workflow and return parameters from the flow', display_name='End Flow', tags=None, icon=None, color=None, group='create', deprecation=None, is_node_group=None), 'library': 'Griptape Nodes Library', 'node_type': 'EndFlow', 'showaddparameter': True, 'size': {'width': 600, 'height': 543}, 'category': 'workflows'}, initial_setup=True)).node_name
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(AddParameterToNodeRequest(parameter_name='sample_output', tooltip='Enter text/string for sample_output.', type='str', input_types=['str'], output_type='str', ui_options={'is_custom': True, 'is_user_added': True}, mode_allowed_input=True, mode_allowed_property=True, mode_allowed_output=True, initial_setup=True))
    node1_name = GriptapeNodes.handle_request(CreateNodeRequest(node_type='MergeTexts', specific_library_name='Griptape Nodes Library', node_name='Merge Texts', metadata={'position': {'x': 1496.3071910286787, 'y': 286.7737096777492}, 'tempId': 'placing-1767391245414-jglkl9', 'library_node_metadata': NodeMetadata(category='text', description='MergeTexts node', display_name='Merge Texts', tags=None, icon='merge', color=None, group='merge', deprecation=None, is_node_group=None), 'library': 'Griptape Nodes Library', 'node_type': 'MergeTexts', 'showaddparameter': False, 'size': {'width': 600, 'height': 500}, 'empty_merge_string_migrated': True}, initial_setup=True)).node_name
    node2_name = GriptapeNodes.handle_request(CreateNodeRequest(node_type='StartFlow', specific_library_name='Griptape Nodes Library', node_name='Start Flow', metadata={'position': {'x': 511.89254711263504, 'y': 392.894280429231}, 'tempId': 'placing-1767396117330-fmclbn', 'library_node_metadata': {'category': 'workflows', 'description': 'Define the start of a workflow and pass parameters into the flow'}, 'library': 'Griptape Nodes Library', 'node_type': 'StartFlow', 'showaddparameter': True, 'size': {'width': 698, 'height': 263}}, resolution='resolved', initial_setup=True)).node_name
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(AddParameterToNodeRequest(parameter_name='sample_input', tooltip='Enter text/string for sample_input.', type='str', input_types=['str'], output_type='str', ui_options={'is_custom': True, 'is_user_added': True}, mode_allowed_input=True, mode_allowed_property=True, mode_allowed_output=True, initial_setup=True))
    GriptapeNodes.handle_request(CreateConnectionRequest(source_node_name=node2_name, source_parameter_name='sample_input', target_node_name=node1_name, target_parameter_name='input_1', initial_setup=True))
    GriptapeNodes.handle_request(CreateConnectionRequest(source_node_name=node1_name, source_parameter_name='output', target_node_name=node0_name, target_parameter_name='sample_output', initial_setup=True))
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='was_successful', node_name=node0_name, value=top_level_unique_values_dict['575ee2e2-1311-4e5c-9b36-c246fb10c037'], initial_setup=True, is_output=False))
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='sample_output', node_name=node0_name, value=top_level_unique_values_dict['3ce44a4a-7494-4025-854c-ae2b0907ea4f'], initial_setup=True, is_output=False))
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='input_1', node_name=node1_name, value=top_level_unique_values_dict['b7057fc6-d824-4b9b-83d3-9a36a347a422'], initial_setup=True, is_output=False))
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='input_2', node_name=node1_name, value=top_level_unique_values_dict['3ce44a4a-7494-4025-854c-ae2b0907ea4f'], initial_setup=True, is_output=False))
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='merge_string', node_name=node1_name, value=top_level_unique_values_dict['b7057fc6-d824-4b9b-83d3-9a36a347a422'], initial_setup=True, is_output=False))
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='whitespace', node_name=node1_name, value=top_level_unique_values_dict['575ee2e2-1311-4e5c-9b36-c246fb10c037'], initial_setup=True, is_output=False))
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='output', node_name=node1_name, value=top_level_unique_values_dict['3ce44a4a-7494-4025-854c-ae2b0907ea4f'], initial_setup=True, is_output=False))
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='output', node_name=node1_name, value=top_level_unique_values_dict['3ce44a4a-7494-4025-854c-ae2b0907ea4f'], initial_setup=True, is_output=True))

def _ensure_workflow_context():
    context_manager = GriptapeNodes.ContextManager()
    if not context_manager.has_current_flow():
        top_level_flow_request = GetTopLevelFlowRequest()
        top_level_flow_result = GriptapeNodes.handle_request(top_level_flow_request)
        if isinstance(top_level_flow_result, GetTopLevelFlowResultSuccess) and top_level_flow_result.flow_name is not None:
            flow_manager = GriptapeNodes.FlowManager()
            flow_obj = flow_manager.get_flow_by_name(top_level_flow_result.flow_name)
            context_manager.push_flow(flow_obj)

def execute_workflow(input: dict, storage_backend: str='local', workflow_executor: WorkflowExecutor | None=None, pickle_control_flow_result: bool=False) -> dict | None:
    return asyncio.run(aexecute_workflow(input=input, storage_backend=storage_backend, workflow_executor=workflow_executor, pickle_control_flow_result=pickle_control_flow_result))

async def aexecute_workflow(input: dict, storage_backend: str='local', workflow_executor: WorkflowExecutor | None=None, pickle_control_flow_result: bool=False) -> dict | None:
    _ensure_workflow_context()
    storage_backend_enum = StorageBackend(storage_backend)
    workflow_executor = workflow_executor or LocalWorkflowExecutor(storage_backend=storage_backend_enum)
    async with workflow_executor as executor:
        await executor.arun(flow_input=input, pickle_control_flow_result=pickle_control_flow_result)
    return executor.output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--storage-backend', choices=['local', 'gtc'], default='local', help="Storage backend to use: 'local' for local filesystem or 'gtc' for Griptape Cloud")
    parser.add_argument('--json-input', default=None, help='JSON string containing parameter values. Takes precedence over individual parameter arguments if provided.')
    parser.add_argument('--exec_out', default=None, help='Connection to the next node in the execution chain')
    parser.add_argument('--sample_input', default=None, help='Enter text/string for sample_input.')
    args = parser.parse_args()
    flow_input = {}
    if args.json_input is not None:
        flow_input = json.loads(args.json_input)
    if args.json_input is None:
        if 'Start Flow' not in flow_input:
            flow_input['Start Flow'] = {}
        if args.exec_out is not None:
            flow_input['Start Flow']['exec_out'] = args.exec_out
        if args.sample_input is not None:
            flow_input['Start Flow']['sample_input'] = args.sample_input
    workflow_output = execute_workflow(input=flow_input, storage_backend=args.storage_backend)
    print(workflow_output)
