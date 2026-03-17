from engine.tools.tool_registry import list_tools


def build_prompt(user_prompt: str, state: dict):

    tools = list_tools()

    tool_descriptions = ""
    for name, tool in tools.items():
        tool_descriptions += f"{name}: {tool['description']}\n"

    steps_text = ""

    for i, step in enumerate(state["steps"]):
        steps_text += f"""
                        Step {i+1}:
                        Action: {step['action']}
                        Parameters: {step['parameters']}
                        Result: {step['result']}
                    """

    return f"""
            You are an AI agent.

            Available tools:
            {tool_descriptions}

            Previous steps:
            {steps_text}

            User request:
            {user_prompt}

            Rules:

            - You can perform multiple steps
            - Use tools if needed
            - ALWAYS include required parameters for tools
            - NEVER call a tool without parameters

            IMPORTANT RULES:

            - Do NOT repeat the same calculation
            - Do NOT recompute results you already obtained
            - Always use previous results instead of recalculating
            - After each step, decide if the task is complete
            - If the final result is already known, respond immediately

            When using a tool, return:

            {{
            "action": "tool_name",
            "parameters": {{
            "required_param": "value"
            }}
            }}

            When the task is completed, you MUST return:

            {{
            "action": "respond",
            "message": "final answer"
            }}

            Return ONLY JSON.
            Do not use markdown.
            """