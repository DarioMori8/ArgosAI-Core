# AI Engine

Questo progetto implementa un **motore di inferenza per modelli di linguaggio (LLM)** eseguiti localmente.

L'obiettivo è costruire una base solida per lo sviluppo di **agenti AI modulari**, che possano utilizzare modelli locali e dati aziendali mantenendo il pieno controllo sull'infrastruttura.

Il sistema espone un'API HTTP che permette di inviare prompt al modello e ricevere risposte generate.

---

## Architettura del sistema

Il sistema è organizzato in più livelli, ognuno con una responsabilità specifica.

```
Client
  ↓
FastAPI Server
  ↓
Request Queue
  ↓
LLM Runtime
  ↓
Inference Engine
  ↓
Model Manager
  ↓
LLM
  ↓
GPU
```

---

## Componenti principali

### `server.py`
Espone l'API HTTP del sistema tramite FastAPI.
Riceve le richieste dei client e le inoltra alla request queue.

---

### `queue_manager.py`
Gestisce la coda delle richieste.
Il server inserisce le richieste nella coda e un worker thread le processa utilizzando il runtime LLM.
Questo permette di gestire più richieste senza bloccare il server.

---

### `runtime.py`
Coordina l'interazione tra il modello e il sistema.
Fornisce un'interfaccia semplice per eseguire generazione di testo utilizzando il modello.

---

### `inference.py`
Contiene la logica di inferenza del modello.

Si occupa di:
- tokenizzazione
- generazione del testo
- decodifica della risposta

---

### `model_manager.py`
Gestisce il caricamento del modello e del tokenizer.

Si occupa di:
- caricare il modello da HuggingFace
- selezionare il device (GPU o CPU)
- rendere disponibili modello e tokenizer al runtime

---

### `config.py`
Centralizza la configurazione del sistema.

Permette di modificare facilmente parametri come:
- modello utilizzato
- parametri di generazione
- configurazione del server

---

### `logger.py`
Gestisce il sistema di logging del progetto.

Traccia informazioni utili come:
- prompt ricevuti
- parametri di generazione
- tempo di inferenza
- lunghezza della risposta

---

## Struttura del progetto

```
ai_engine
│
├── engine
│   ├── config.py
│   ├── logger.py
│   ├── server.py
│   ├── runtime.py
│   ├── inference.py
│   ├── model_manager.py
│   └── queue_manager.py
│
├── scripts
│   ├── test_model.py
│   └── test_api.py
│
├── requirements.txt
└── README.md
```

---

## Avviare il server

Attivare l'ambiente virtuale:

```bash
source venv/bin/activate
```

Avviare il server:

```bash
uvicorn engine.server:app --host 0.0.0.0 --port 8000
```

---

## Test dell'API

Aprire nel browser:

```
http://localhost:8000/docs
```

Oppure utilizzare lo script:

```bash
python scripts/test_api.py
```

---

## Obiettivo del progetto

Questo progetto rappresenta la base di un **Core Engine per agenti AI**.

Le evoluzioni future includeranno:

- supporto a più modelli
- routing intelligente delle richieste
- integrazione con tool esterni
- memoria per agenti AI
- integrazione con dati aziendali