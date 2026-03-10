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



from engine.model.model_manager import ModelManager
from engine.inference.inference import generate_text
from engine.runtime.prompt_builder import build_prompt
from engine.runtime.json_parser import parse_json_response
from engine.runtime.validator import validate_output
from engine.logging.logger import log_request, log_response, log_error
from engine.tools.tool_executor import execute_tool

class LLMRuntime:

    def __init__(self, model_name):

        self.model_manager = ModelManager(model_name)

        self.model = self.model_manager.get_model()
        self.tokenizer = self.model_manager.get_tokenizer()
        self.device = self.model_manager.get_device()

    def generate(self, prompt, temperature, max_tokens, top_p):

        structured_prompt = build_prompt(prompt)
        
        response = generate_text(
            self.model,
            self.tokenizer,
            self.device,
            structured_prompt,
            temperature,
            max_tokens,
            top_p
        )

        json_response = parse_json_response(response)

        if json_response is None:
            log_error("Invalid JSON response", f"Raw response: {response}")
            return {"error": "Model did not return valid JSON", "raw_response": response}
        validated_response = validate_output(json_response)

        if validated_response is None:
            log_error("Invalid output format", f"Raw response: {response}")
            return {"error": "Invalid output format from model", "raw_response": response}

        if validated_response.action == "respond":
            return validated_response.dict()

        # se è un tool lo eseguiamo
        tool_result = execute_tool(validated_response.action, validated_response.parameters or {})
        if "error" in tool_result:
            return {
                "action": "respond",
                "message": f"Tool error: {tool_result['error']}"
            }

        # secondo passaggio LLM
        followup_prompt =  f"""
            You are an AI agent.

            The user asked:
            {prompt}

            A tool was used to answer the request.

            Tool name:
            {validated_response.action}

            Tool result:
            {tool_result}

            Your task:
            Generate the final response for the user.

            Return ONLY JSON in this format:

            {{
            "action": "respond",
            "message": "final answer for the user"
            }}

            Do not include markdown.
            Do not include explanations.
            Return only valid JSON.
            """

        raw_final = generate_text(
            self.model,
            self.tokenizer,
            self.device,
            followup_prompt,
            temperature,
            max_tokens,
            top_p
        )

        final_json = parse_json_response(raw_final)

        if final_json is None:
            log_error("Invalid final JSON", raw_final)
            return {"error": "invalid_final_json"}

        validated_final = validate_output(final_json)

        if validated_final is None:
            log_error("Invalid final output format", raw_final)
            return {"error": "invalid_final_output"}

        return validated_final.dict(exclude_none=True)