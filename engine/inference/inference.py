"""
INFERENCE MODULE

Questo modulo contiene la logica di inferenza pura del modello LLM.

Il suo compito è prendere un prompt testuale, trasformarlo in tensori tramite
il tokenizer, eseguire la generazione del testo con il modello e convertire
l'output del modello in una risposta leggibile.

Responsabilità principali:
- Tokenizzare il prompt in input
- Spostare i tensori sul device corretto (GPU/CPU)
- Eseguire la generazione del testo tramite model.generate()
- Applicare i parametri di generazione (temperature, top_p, max_tokens)
- Decodificare l'output del modello in testo

Questo modulo non conosce nulla dell'architettura del server o della gestione
delle richieste. Si occupa esclusivamente della fase di inferenza del modello.

In futuro questo componente potrà essere esteso per:
- Gestire batching di più richieste
- Implementare streaming dei token
- Integrare KV cache per velocizzare la generazione
- Supportare diversi backend di inferenza (vLLM, TensorRT, ecc.)
"""



def generate_text(model, tokenizer, device, prompt, temperature, max_tokens, top_p):

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    input_length = inputs["input_ids"].shape[1]

    output = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p
    )

    generated_tokens = output[0][input_length:]

    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    return response