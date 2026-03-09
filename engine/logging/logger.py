"""
LOGGER MODULE

Questo modulo gestisce il sistema di logging del progetto.
Centralizza la configurazione dei log e fornisce funzioni
per tracciare le richieste e le risposte del sistema AI.

L'obiettivo è rendere il comportamento del server osservabile
senza utilizzare semplici print.
"""

import logging
import time


# configurazione base del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("ai_engine")


def log_request(prompt, temperature, max_tokens, top_p):

    logger.info("NEW REQUEST")

    logger.info(f"Prompt: {prompt}")
    logger.info(f"Temperature: {temperature}")
    logger.info(f"Max tokens: {max_tokens}")
    logger.info(f"Top_p: {top_p}")

    return time.time()


def log_response(start_time, response):

    duration = time.time() - start_time

    token_count = len(str(response).split())

    logger.info("RESPONSE GENERATED")

    logger.info(f"Response length (words): {token_count}")
    logger.info(f"Inference time: {duration:.2f} seconds")


def log_error(error_type, details):

    logger.error("RUNTIME ERROR")

    logger.error(f"Error type: {error_type}")

    logger.error(f"Details: {details}")