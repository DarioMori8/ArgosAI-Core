"""
TOOL REGISTRY

Questo modulo mantiene il registro dei tool disponibili
per il runtime.

Permette di registrare tool dinamicamente e recuperarli
quando il modello richiede un'azione.
"""

TOOLS = {}


def register_tool(name, function):
    """
    Registra un nuovo tool nel registry.
    """

    TOOLS[name] = function


def get_tool(name):
    """
    Restituisce il tool richiesto.
    """

    return TOOLS.get(name)

import engine.tools.calculator_tool