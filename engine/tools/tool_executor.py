"""
TOOL EXECUTOR

Questo modulo esegue i tool richiesti dal modello.
"""

from engine.tools.tool_registry import get_tool


def execute_tool(action, parameters):

    tool = get_tool(action)

    if tool is None:
        return {"error": f"Tool '{action}' not found"}

    try:
        return tool(**parameters)

    except Exception as e:
        return {"error": str(e)}