"""
TOOL REGISTRY

Questo modulo mantiene la lista dei tool disponibili
per il runtime.
"""

from engine.tools.calculator_tool import run as calculator


TOOLS = {
    "calculator": calculator
}