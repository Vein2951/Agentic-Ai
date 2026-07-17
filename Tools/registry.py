from .calculator import execute as calculator
from .time_tool import execute as time_tool
from .weather import execute as weather_tool
from .currency_converter import execute as currency_converter_tool
from .unit_converter import execute as unit_converter_tool

tools = {
    "calculator": calculator,
    "time": time_tool,
    "weather": weather_tool,
    "currency_converter": currency_converter_tool,
    "unit_converter": unit_converter_tool,
}


def execute_tool(tool_name, arguments):
    tool = tools.get(tool_name)

    if tool is None:
        return {"error": f"Tool '{tool_name}' not found."}

    return tool(arguments)


def list_tools():
    return list(tools.keys())


if __name__ == "__main__":
    print("Registered tools\n")

    print(
        execute_tool(
            "calculator",
            {"expression": "2 + 2"}
        )
    )

    print()

    print(
        execute_tool(
            "time",
            {}
        )
    )

    print()

    print(
        execute_tool(
            "weather",
            {"city": "New York"}
        )
    )