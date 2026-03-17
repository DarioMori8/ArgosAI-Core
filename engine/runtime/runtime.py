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
from engine.logging.logger import log_agent_decision, log_request, log_response, log_error, log_tool_result
from engine.tools.tool_executor import execute_tool

class LLMRuntime:

    def __init__(self, model_name):

        self.model_manager = ModelManager(model_name)

        self.model = self.model_manager.get_model()
        self.tokenizer = self.model_manager.get_tokenizer()
        self.device = self.model_manager.get_device()

    def generate(self, prompt, temperature, max_tokens, top_p):

        state = {
            "steps": []
        }

        max_steps = 5

        for step in range(max_steps):

            structured_prompt = build_prompt(prompt, state)

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
                return {"error": "invalid_json", "raw": response}

            validated = validate_output(json_response)

            if validated is None:
                log_error("Invalid output format", f"Raw response: {response}")
                return {"error": "invalid_format", "raw": response}

            log_agent_decision(
                step + 1,
                validated.action,
                validated.parameters
            )

            # CASO 1: risposta finale già ottenuta in uno step precedente → STOP

            if len(state["steps"]) >= 2:
                last_step = state["steps"][-1]
                prev_step = state["steps"][-2]

                if (
                    last_step["action"] == validated.action and
                    last_step["parameters"] == validated.parameters and
                    last_step["result"] == prev_step["result"]
                ):
                    return {
                        "action": "respond",
                        "message": f"Final result: {last_step['result']}"
                    }

            # CASO 1: risposta finale → STOP
            if validated.action == "respond":
                return validated.dict(exclude_none=True)

            # CASO 2: esegue tool
            tool_result = execute_tool(validated.action, validated.parameters or {})

            if "error" in tool_result:
                return {
                    "action": "respond",
                    "message": f"Tool error: {tool_result['error']}"
                }
      
                    
            log_tool_result(
                step + 1,
                tool_result
            )

            # salva lo step
            state["steps"].append({
                "action": validated.action,
                "parameters": validated.parameters,
                "result": tool_result
            })

        return {
            "action": "respond",
            "message": "Max steps reached without a final answer"
        }