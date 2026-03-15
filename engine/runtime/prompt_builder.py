from engine.tools.tool_registry import list_tools


def build_prompt(user_prompt: str):

    tools = list_tools()

    tool_descriptions = ""

    for name, tool in tools.items():
        tool_descriptions += f"{name}: {tool['description']}\n"

    system_instruction = f"""
        You are an AI agent.

        You can use the following tools:

        {tool_descriptions}

        Rules:

        1. If a tool is needed, return JSON in this format:

        {{
        "action": "tool_name",
        "parameters": {{
        "param": "value"
        }}
        }}

        2. If no tool is needed, return:

        {{
        "action": "respond",
        "message": "your response"
        }}

        Return ONLY JSON.
        Do not use markdown.
        """

    return f"{system_instruction}\nUser request: {user_prompt}\n"