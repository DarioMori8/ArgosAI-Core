"""
LLM RUNTIME

Questo modulo rappresenta il motore operativo del sistema AI.

Il runtime coordina l'interazione tra i componenti che gestiscono il modello
(Model Manager) e quelli che eseguono l'inferenza (Inference module).

Responsabilità principali:
- Inizializzare il Model Manager
- Ottenere modello, tokenizer e device
- Esporre un metodo semplice per generare testo a partire da un prompt
- Coordinare la pipeline di generazione tra i diversi moduli

Il runtime è il punto centrale dove la logica di generazione viene orchestrata.

Il server API non interagisce direttamente con il modello ma utilizza il runtime
come interfaccia per eseguire operazioni AI.

In futuro questo componente diventerà il cuore del Core Engine e potrà gestire:
- orchestrazione di più modelli
- routing delle richieste verso modelli diversi
- gestione di agenti AI
- tool execution
- memoria conversazionale
- batching automatico delle richieste
"""



from engine.model_manager import ModelManager
from engine.inference import generate_text


class LLMRuntime:

    def __init__(self, model_name):

        self.model_manager = ModelManager(model_name)

        self.model = self.model_manager.get_model()
        self.tokenizer = self.model_manager.get_tokenizer()
        self.device = self.model_manager.get_device()

    def generate(self, prompt, temperature, max_tokens, top_p):

        response = generate_text(
            self.model,
            self.tokenizer,
            self.device,
            prompt,
            temperature,
            max_tokens,
            top_p
        )

        return response