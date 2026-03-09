import json
import re


def parse_json_response(text: str):

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group())

    except Exception:
        return None