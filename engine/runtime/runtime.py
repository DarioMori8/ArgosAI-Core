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


# numero massimo di step identici consecutivi prima di considerare il loop
MAX_IDENTICAL_STEPS = 2


def _is_same_step(step_a: dict, step_b: dict) -> bool:
    """Controlla se due step sono identici per action e parameters."""
    return (
        step_a["action"] == step_b["action"] and
        step_a["parameters"] == step_b["parameters"]
    )


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

        # contatore step identici consecutivi
        identical_step_count = 0
        last_action = None
        last_parameters = None

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

            # --- RILEVAMENTO LOOP ---
            # Confronta la decisione corrente con quella precedente.
            # Se il modello ripete la stessa action+parameters per MAX_IDENTICAL_STEPS
            # volte di fila, interrompe il ciclo e restituisce l'ultimo risultato noto.

            current_action = validated.action
            current_parameters = validated.parameters

            if (
                current_action == last_action and
                current_parameters == last_parameters
            ):
                identical_step_count += 1
            else:
                identical_step_count = 1

            last_action = current_action
            last_parameters = current_parameters

            if identical_step_count > MAX_IDENTICAL_STEPS:

                log_error(
                    "loop_detected",
                    f"Step identico ripetuto {identical_step_count} volte: "
                    f"action={current_action}, parameters={current_parameters}"
                )

                # restituisce l'ultimo risultato disponibile, se esiste
                if state["steps"]:
                    last_result = state["steps"][-1]["result"]
                    return {
                        "action": "respond",
                        "message": f"Final result: {last_result}"
                    }

                return {
                    "action": "respond",
                    "message": "Loop detected without results"
                }

            # --- FINE RILEVAMENTO LOOP ---

            # risposta finale → STOP
            if validated.action == "respond":
                return validated.dict(exclude_none=True)

            # esegue il tool
            tool_result = execute_tool(validated.action, validated.parameters or {})

            if "error" in tool_result:
                return {
                    "action": "respond",
                    "message": f"Tool error: {tool_result['error']}"
                }

            log_tool_result(step + 1, tool_result)

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