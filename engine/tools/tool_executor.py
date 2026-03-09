"""
TOOL EXECUTOR

Questo modulo esegue i tool richiesti dal modello.
"""

from engine.tools.tool_registry import TOOLS


def execute_tool(action, parameters):

    if action not in TOOLS:
        return {"error": f"Tool '{action}' not found"}

    tool_function = TOOLS[action]

    try:
        return tool_function(**parameters)

    except Exception as e:
        return {"error": str(e)}