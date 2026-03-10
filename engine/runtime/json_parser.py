import json
import re


def parse_json_response(text: str):

    if not text:
        return None

    # rimuove blocchi markdown ```json ```
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # rimuove spazi iniziali/finali
    text = text.strip()

    # trova il primo JSON valido
    start = text.find("{")

    while start != -1:

        end = text.find("}", start)

        while end != -1:
            candidate = text[start:end+1]

            try:
                return json.loads(candidate)
            except Exception:
                end = text.find("}", end+1)

        start = text.find("{", start+1)

    return None