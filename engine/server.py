"""
API SERVER

Questo modulo espone l'interfaccia HTTP del sistema tramite FastAPI.

Il server non contiene logica di inferenza o gestione dei modelli.
Il suo unico compito è ricevere richieste HTTP, validarle e inoltrarle
al runtime tramite il sistema di queue.

Responsabilità principali:
- Esporre endpoint API per l'inferenza
- Validare i dati in ingresso tramite Pydantic
- Inviare le richieste alla Request Queue
- Restituire la risposta al client

Il server rappresenta il punto di accesso esterno al sistema.

Separare il server dal runtime permette di mantenere l'architettura
modulare e scalabile.

In futuro questo componente potrà essere esteso per:
- autenticazione delle richieste
- rate limiting
- logging delle richieste
- monitoraggio del sistema
- gestione di più endpoint per agenti AI
"""

from fastapi import FastAPI
from pydantic import BaseModel
import threading

from engine.runtime import LLMRuntime
from engine.queue_manager import RequestQueue
from engine.config import Config

MODEL_NAME = Config.MODEL_NAME

app = FastAPI()


print("Starting AI runtime...")

runtime = LLMRuntime(MODEL_NAME)
queue = RequestQueue(runtime)

print("Runtime ready")


class PromptRequest(BaseModel):
    prompt: str
    temperature: float=Config.DEFAULT_TEMPERATURE
    max_tokens: int=Config.DEFAULT_MAX_TOKENS
    top_p: float=Config.DEFAULT_TOP_P


@app.post("/generate")
def generate(request: PromptRequest):

    result = {}

    event = threading.Event() 

    def callback(response):
        result["response"] = response
        event.set()

    queue.submit(
        prompt=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        top_p=request.top_p,
        callback=callback
    )

    event.wait()

    return result