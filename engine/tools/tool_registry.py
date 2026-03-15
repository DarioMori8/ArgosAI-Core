"""
TOOL REGISTRY

Mantiene il registro dei tool disponibili per il runtime.
Ogni tool ha nome, funzione e descrizione.
"""

TOOLS = {}


def register_tool(name, function, description):
    TOOLS[name] = {
        "function": function,
        "description": description
    }


def get_tool(name):
    tool = TOOLS.get(name)

    if tool:
        return tool["function"]

    return None


def list_tools():
    return TOOLS


# importa i tool per registrarli
import engine.tools.calculator_tool