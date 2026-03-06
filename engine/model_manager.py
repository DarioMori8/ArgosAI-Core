"""
MODEL MANAGER

Questo modulo è responsabile della gestione dei modelli di linguaggio (LLM)
utilizzati dal sistema.

Il suo compito principale è caricare il modello e il tokenizer da HuggingFace,
configurare il device corretto (GPU o CPU) e rendere disponibili queste risorse
agli altri componenti del sistema.

Responsabilità principali:
- Caricare il modello LLM dal repository HuggingFace o dalla cache locale
- Caricare e configurare il tokenizer
- Selezionare automaticamente il device (GPU se disponibile)
- Spostare il modello sulla GPU
- Fornire accesso a model, tokenizer e device al resto del runtime

Questo modulo rappresenta il livello più basso della gestione dei modelli.
Non contiene logica di inferenza né logica applicativa.

In futuro questo componente potrà evolvere per:
- Gestire più modelli contemporaneamente
- Implementare caching dei modelli
- Gestire la memoria GPU (VRAM)
- Caricare modelli specifici per cliente
- Supportare quantizzazione (4bit/8bit)
"""


from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class ModelManager:

    def __init__(self, model_name, model_class=AutoModelForCausalLM):
        self.model_name = model_name
        self.model_class = model_class
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading tokenizer for {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        print(f"Loading model {model_name}")

        self.model = self.model_class.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )

        self.model.to(self.device)

        print("Model ready")

    def get_model(self):
        return self.model

    def get_tokenizer(self):
        return self.tokenizer

    def get_device(self):
        return self.device