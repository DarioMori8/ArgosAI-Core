import json
import re


def parse_json_response(text: str):
    """
    Estrae il primo oggetto JSON valido da una stringa di testo.

    Usa json.JSONDecoder().raw_decode() per gestire correttamente:
    - JSON annidati (es. parameters: {key: value})
    - Testo prima/dopo il JSON
    - Blocchi markdown ```json ```
    - Spazi e newline extra

    Ritorna il dizionario Python se trovato, None altrimenti.
    """

    if not text:
        return None

    # rimuove blocchi markdown ```json ```
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    decoder = json.JSONDecoder()

    # scansiona il testo cercando il primo '{' valido
    start = text.find("{")

    while start != -1:

        try:
            # raw_decode ritorna (oggetto, indice_fine)
            # gestisce correttamente la profondità delle parentesi graffe
            obj, _ = decoder.raw_decode(text, start)
            return obj

        except json.JSONDecodeError:
            # questo '{' non è l'inizio di un JSON valido, proviamo il prossimo
            start = text.find("{", start + 1)

    return None