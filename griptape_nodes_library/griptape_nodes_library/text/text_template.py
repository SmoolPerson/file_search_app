from typing import Any

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import DataNode


class TextTemplate(DataNode):
    def __init__(
        self,
        name: str,
        metadata: dict[Any, Any] | None = None,
    ) -> None:
        super().__init__(name, metadata)

        # Add template parameter
        self.add_parameter(
            Parameter(
                name="template",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="Hello {var1}, welcome to {var2}!",
                input_types=["str"],
                type="str",
                tooltip="Template string with placeholders like {var1}, {var2}, etc.",
                ui_options={"multiline": True},
            )
        )

        # Add multiple input parameters for variables
        self.add_parameter(
            Parameter(
                name="var1",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                tooltip="Value to insert for {var1} placeholder.",
            )
        )
        self.add_parameter(
            Parameter(
                name="var2",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                tooltip="Value to insert for {var2} placeholder.",
            )
        )
        self.add_parameter(
            Parameter(
                name="var3",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                tooltip="Value to insert for {var3} placeholder.",
            )
        )
        self.add_parameter(
            Parameter(
                name="var4",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                tooltip="Value to insert for {var4} placeholder.",
            )
        )
        self.add_parameter(
            Parameter(
                name="var5",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                tooltip="Value to insert for {var5} placeholder.",
            )
        )
        self.add_parameter(
            Parameter(
                name="var6",
                allowed_modes={ParameterMode.INPUT, ParameterMode.PROPERTY},
                default_value="",
                input_types=["str", "int", "float", "bool"],
                tooltip="Value to insert for {var6} placeholder.",
            )
        )

        # Add output parameter
        self.add_parameter(
            Parameter(
                name="output",
                allowed_modes={ParameterMode.OUTPUT},
                output_type="str",
                default_value="",
                tooltip="The formatted text with variables inserted.",
                ui_options={"multiline": True},
            )
        )

    def _format_template(self) -> str:
        """Format the template string with the provided variables."""
        template = self.parameter_values.get("template", "")

        if not template:
            return ""

        # Collect all variable values
        var_values = {}
        for i in range(1, 7):
            var_name = f"var{i}"
            value = self.parameter_values.get(var_name, "")
            if value is None:
                value = ""
            var_values[var_name] = str(value)

        try:
            formatted_text = template.format(**var_values)
            return formatted_text
        except KeyError:
            return ""
        except Exception:
            return template

    def after_value_set(self, parameter: Parameter, value: Any) -> None:
        if parameter.name != "output":
            result = self._format_template()
            self.parameter_output_values["output"] = result
            self.set_parameter_value("output", result)
        return super().after_value_set(parameter, value)

    def process(self) -> None:
        result = self._format_template()
        self.parameter_output_values["output"] = result