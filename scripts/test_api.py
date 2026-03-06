"""
API TEST SCRIPT

Questo script invia richieste HTTP al server AI locale per testare
il funzionamento dell'endpoint di generazione.

È utile per:
- verificare che il server sia attivo
- testare rapidamente il comportamento del modello
- eseguire benchmark o stress test
- simulare richieste client senza usare il browser
"""

import requests
import time


URL = "http://localhost:8000/generate"


payload = {
    "prompt": "Explain artificial intelligence in simple terms.",
    "temperature": 0.7,
    "max_tokens": 150,
    "top_p": 0.9
}

for i in range(5):

    start = time.time()

    response = requests.post(URL, json=payload)

    end = time.time()

    print(response.json())

    print("Request", i+1, "time:", round(end-start,2))

