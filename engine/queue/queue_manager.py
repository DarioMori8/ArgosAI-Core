"""
REQUEST QUEUE MANAGER

Questo modulo implementa una coda di richieste per il sistema di inferenza.

L'obiettivo è evitare che il server API esegua direttamente le operazioni di
generazione del modello, che sono costose e bloccanti.

Il server inserisce le richieste nella coda e un worker dedicato le esegue
in sequenza utilizzando il runtime LLM.

Responsabilità principali:
- Gestire una coda di richieste di generazione
- Eseguire le richieste tramite un worker thread
- Garantire che le richieste vengano processate in ordine
- Restituire la risposta al chiamante tramite callback

Questo approccio permette al server di accettare più richieste
contemporaneamente senza bloccare il thread principale.

In futuro questo componente potrà evolvere per:
- supportare più worker
- implementare batching automatico
- gestire priorità delle richieste
- distribuire il carico su più GPU
"""

from queue import Queue
import threading
from engine.logging.logger import log_request, log_response

class RequestQueue:

    def __init__(self, runtime):

        self.runtime = runtime
        self.queue = Queue()

        worker = threading.Thread(target=self.worker_loop, daemon=True)
        worker.start()

    def worker_loop(self):

        while True:

            request = self.queue.get()

            prompt = request["prompt"]
            temperature = request["temperature"]
            max_tokens = request["max_tokens"]
            top_p = request["top_p"]
            callback = request["callback"]
            start_time = log_request(prompt, temperature, max_tokens, top_p)

            response = self.runtime.generate(
                prompt,
                temperature,
                max_tokens,
                top_p
            )
            log_response(start_time, response)

            callback(response)

            self.queue.task_done()

    def submit(self, prompt, temperature, max_tokens, top_p, callback):

        self.queue.put({
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "callback": callback
        })