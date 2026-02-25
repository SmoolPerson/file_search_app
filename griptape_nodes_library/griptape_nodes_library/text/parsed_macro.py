from typing import Any

from griptape_nodes.common.macro_parser.core import ParsedMacro
from griptape_nodes.common.macro_parser.exceptions import MacroResolutionError, MacroSyntaxError
from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import DataNode
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes


class ParsedMacroNode(DataNode):
    """Node for parsing and resolving macro templates.

    This node uses the ParsedMacro class to resolve template strings with variables.
    """

    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
    ) -> None:
        super().__init__(name, metadata)

        # Template parameter
        self.add_parameter(
            Parameter(
                name="template",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="{var1}/{var2}",
                input_types=["str"],
                type="str",
                tooltip="Macro template string with variables in curly braces. Example: {var1}/{var2}",
                ui_options={"multiline": True},
            )
        )

        # Variable inputs
        self.add_parameter(
            Parameter(
                name="var1",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                type="str",
                tooltip="Value for var1 variable",
            )
        )

        self.add_parameter(
            Parameter(
                name="var2",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                type="str",
                tooltip="Value for var2 variable",
            )
        )

        self.add_parameter(
            Parameter(
                name="var3",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                type="str",
                tooltip="Value for var3 variable",
            )
        )

        self.add_parameter(
            Parameter(
                name="var4",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                type="str",
                tooltip="Value for var4 variable",
            )
        )

        # Output parameter
        self.add_parameter(
            Parameter(
                name="result",
                allowed_modes={ParameterMode.OUTPUT},
                output_type="str",
                default_value="",
                tooltip="The resolved template string",
                ui_options={"multiline": True},
            )
        )

    def _resolve_template(self) -> str:
        """Resolve the template with the provided variables.

        Returns:
            The resolved template string, or an error message if resolution fails
        """
        template_str = self.get_parameter_value("template")

        if not template_str:
            return ""

        # Collect variable values
        variables = {}
        for i in range(1, 5):
            var_name = f"var{i}"
            value = self.get_parameter_value(var_name)
            if value is None:
                value = ""
            variables[var_name] = str(value)

        try:
            parsed_macro = ParsedMacro(template_str)
        except MacroSyntaxError as e:
            return f"Error: Failed to parse template - {e}"

        # Get secrets manager
        secrets_manager = GriptapeNodes.SecretsManager()

        try:
            result = parsed_macro.resolve(variables, secrets_manager)
            return result
        except MacroResolutionError as e:
            return f"Error: {e}"

    def after_value_set(self, parameter: Parameter, value: Any) -> None:
        if parameter.name != "result":
            result = self._resolve_template()
            self.parameter_output_values["result"] = result
            self.set_parameter_value("result", result)
        return super().after_value_set(parameter, value)

    def process(self) -> None:
        result = self._resolve_template()
        self.parameter_output_values["result"] = result
