"""
OUTPUT VALIDATOR

Questo modulo valida il JSON prodotto dal modello
rispetto allo schema AgentOutput.
"""

from engine.schemas.agent_output import AgentOutput


def validate_output(data):

    try:

        validated = AgentOutput(**data)

        return validated

    except Exception:

        return None