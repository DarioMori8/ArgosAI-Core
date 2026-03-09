"""
AGENT OUTPUT SCHEMA

Questo schema definisce il formato strutturato che il modello LLM
deve restituire al runtime.

L'obiettivo è evitare output testuali liberi e costringere il modello
a produrre una struttura JSON valida che possa essere interpretata
dal sistema.

Questo schema rappresenta il primo passo verso un runtime per agenti AI.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class AgentOutput(BaseModel):

    action: str

    message: Optional[str] = None

    parameters: Optional[Dict[str, Any]] = None