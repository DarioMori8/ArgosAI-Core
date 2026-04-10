# AI Engine

AI Engine è un **runtime per modelli di linguaggio (LLM) eseguiti localmente** progettato per essere la base di un **Core Engine per agenti AI modulari**.

A differenza di un semplice sistema di inferenza, questo progetto permette ai modelli di linguaggio di:

- interpretare richieste in linguaggio naturale
- produrre output strutturato in formato JSON
- decidere azioni da eseguire
- utilizzare strumenti esterni (tools)
- integrare i risultati degli strumenti nella risposta finale

L'obiettivo del progetto è costruire un'infrastruttura modulare per **agenti AI locali**, che possano operare su dati aziendali mantenendo il pieno controllo sull'infrastruttura e sulla privacy dei dati.

---

## Architettura del sistema

Il sistema è progettato come una pipeline modulare in cui ogni componente ha una responsabilità specifica.

```
Client
↓
FastAPI Server
↓
Request Queue
↓
LLM Runtime
↓
Prompt Builder
↓
LLM
↓
JSON Parser
↓
Output Validator
↓
Tool Executor
↓
Tool Registry
↓
Tools
↓
LLM (final reasoning)
```

Il modello non esegue direttamente operazioni deterministiche ma produce **output strutturato JSON** che viene interpretato dal runtime per eseguire azioni specifiche.

Questo approccio permette di combinare:

- **capacità di ragionamento dei modelli AI**
- **esecuzione deterministica del software**

---

## Agent Execution Flow

Il flusso di esecuzione di una richiesta segue questi passaggi:

1. L'utente invia una richiesta al sistema.
2. Il prompt builder costruisce il prompt includendo le informazioni sui tool disponibili.
3. Il modello analizza la richiesta e restituisce un output JSON strutturato.
4. Il runtime valida il JSON ricevuto.
5. Se viene richiesto un tool, il runtime esegue lo strumento appropriato.
6. Il risultato del tool viene fornito nuovamente al modello.
7. Il modello genera la risposta finale per l'utente.

Questo meccanismo permette agli agenti AI di **integrare strumenti esterni nel processo di ragionamento**.

---

## Componenti principali

### `server.py`

Espone l'API HTTP del sistema tramite FastAPI.

Responsabilità principali:

- ricevere richieste dai client
- validare i parametri della richiesta
- inviare la richiesta alla coda di esecuzione

---

### `queue_manager.py`

Gestisce una coda di richieste per evitare che il server HTTP venga bloccato da operazioni di inferenza.

Il server inserisce le richieste nella coda e un worker thread le processa utilizzando il runtime LLM.

---

### `runtime.py`

Rappresenta il **motore operativo del sistema**.

Coordina l'interazione tra:

- il modello LLM
- il parser JSON
- il sistema di validazione
- il sistema di tool execution

Il runtime implementa il **reasoning loop** degli agenti.

---

### `prompt_builder.py`

Costruisce il prompt inviato al modello.

Include informazioni su:

- richiesta dell'utente
- strumenti disponibili
- formato JSON richiesto per l'output

Questo permette al modello di sapere **quali strumenti può utilizzare**.

---

### `json_parser.py`

Estrae il JSON dall'output del modello.

Gli LLM possono restituire output con formattazione non prevista (markdown, testo extra).  
Questo modulo identifica e restituisce il **primo JSON valido**.

---

### `validator.py`

Valida l'output JSON prodotto dal modello utilizzando uno schema Pydantic.

Garantisce che il runtime riceva dati strutturati e coerenti.

---

### `tool_executor.py`

Esegue i tool richiesti dal modello.

Riceve l'azione dal JSON generato dal modello e chiama la funzione associata nel registry dei tool.

---

### `tool_registry.py`

Mantiene il registro dei tool disponibili nel sistema.

Permette di registrare nuovi strumenti dinamicamente senza modificare il runtime.

---

### `calculator_tool.py`

Esempio di tool integrato nel sistema.

Esegue espressioni matematiche utilizzando il modulo `ast` per garantire un'esecuzione sicura, evitando l'utilizzo di `eval`.

---

### `inference.py`

Contiene la logica di inferenza del modello.

Responsabilità principali:

- tokenizzazione del prompt
- generazione del testo
- decodifica dell'output del modello

---

### `model_manager.py`

Gestisce il caricamento del modello e del tokenizer.

Si occupa di:

- caricare il modello da HuggingFace
- selezionare automaticamente il device (GPU o CPU)
- rendere disponibili modello e tokenizer al runtime

---

### `config.py`

Centralizza la configurazione del sistema.

Permette di modificare facilmente:

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
- errori del runtime

---

## Struttura del progetto

```
ai_engine
│
├── engine
│   │
│   ├── api
│   │   └── server.py
│   │
│   ├── config
│   │   └── config.py
│   │
│   ├── logging
│   │   └── logger.py
│   │
│   ├── model
│   │   └── model_manager.py
│   │
│   ├── inference
│   │   └── inference.py
│   │
│   ├── runtime
│   │   ├── runtime.py
│   │   ├── prompt_builder.py
│   │   ├── json_parser.py
│   │   └── validator.py
│   │
│   ├── queue
│   │   └── queue_manager.py
│   │
│   └── tools
│       ├── tool_registry.py
│       ├── tool_executor.py
│       └── calculator_tool.py
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
uvicorn engine.api.server:app --host 0.0.0.0 --port 8000
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

Questo progetto rappresenta la base di un Core Engine per agenti AI locali.

L'obiettivo è sviluppare una piattaforma che permetta alle aziende di utilizzare modelli di linguaggio:

- completamente **on-premise**
- integrati con **strumenti software aziendali**
- con massima **trasparenza e controllo** del processo decisionale