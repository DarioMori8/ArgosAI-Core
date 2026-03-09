"""
PROMPT BUILDER

Questo modulo costruisce il prompt che viene inviato al modello.

Il suo scopo è fornire istruzioni chiare al LLM affinché produca
un output strutturato in formato JSON conforme allo schema definito
dal runtime.
"""


def build_prompt(user_prompt: str) -> str:

    return f"""
            You are an AI system that must return ONLY JSON.

            Allowed actions:
            - respond
            - calculator

            JSON schema:

            {{
            "action": "respond",
            "message": "text response"
            }}

            OR

            {{
            "action": "calculator",
            "parameters": {{
            "expression": "math expression"
            }}
            }}

            Return ONLY valid JSON.
            Do not add explanations.

            User request:
            {user_prompt}

            JSON:
            """