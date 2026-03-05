from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_model(model_name, model_class=AutoModelForCausalLM):

    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Loading model {model_name} on {device}...")

    model = model_class.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )

    model.to(device)

    print("Model loaded successfully")

    return model, tokenizer, device