"""
SYSTEM CONFIGURATION

Questo modulo centralizza tutti i parametri di configurazione del sistema.
L'obiettivo è evitare valori "hard-coded" sparsi nei file del progetto.

Tutti i componenti del sistema (server, runtime, inference) possono
importare questo file per ottenere le configurazioni principali.

Questo approccio rende il sistema più facile da modificare e mantenere.
"""


class Config:

    # modello LLM utilizzato
    MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
    # parametri di generazione di default
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 150
    DEFAULT_TOP_P = 0.9

    # configurazione server
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 8000