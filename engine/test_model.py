import torch
from model_loader import load_model

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
# carica modello
model, tokenizer, device = load_model(MODEL_NAME)

prompts = [
    "Explain what artificial intelligence is.",
    "Explain what machine learning is.",
    "Explain what neural networks are.",
    "Explain what deep learning is."
]

# tokenizzazione
inputs = tokenizer(prompts, return_tensors="pt",padding=True)

# sposta input sullo stesso device del modello
inputs = {k: v.to(device) for k, v in inputs.items()}

print("Generating response...\n")

output = model.generate(
    **inputs,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
)

response = tokenizer.decode(output[0], skip_special_tokens=True)

print("MODEL RESPONSE:\n")
print(response)