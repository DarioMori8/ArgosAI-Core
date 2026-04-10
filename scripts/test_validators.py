"""
TEST SUITE — Settimana 1

Test unitari per:
- json_parser.parse_json_response()
- validator.validate_output()

Esegui con: pytest scripts/test_validators.py -v
"""

import pytest
import sys
import os

# aggiunge la root del progetto al path in modo da importare i moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.runtime.json_parser import parse_json_response
from engine.runtime.validator import validate_output


# ─────────────────────────────────────────────
# TEST: parse_json_response
# ─────────────────────────────────────────────

class TestParseJsonResponse:

    def test_simple_json(self):
        text = '{"action": "respond", "message": "done"}'
        result = parse_json_response(text)
        assert result == {"action": "respond", "message": "done"}

    def test_json_with_nested_parameters(self):
        """Caso critico: JSON annidato con parameters — il vecchio parser falliva."""
        text = '{"action": "calculator", "parameters": {"expression": "2 + 2"}}'
        result = parse_json_response(text)
        assert result == {
            "action": "calculator",
            "parameters": {"expression": "2 + 2"}
        }

    def test_json_wrapped_in_markdown(self):
        text = '```json\n{"action": "respond", "message": "hello"}\n```'
        result = parse_json_response(text)
        assert result == {"action": "respond", "message": "hello"}

    def test_json_with_text_before_and_after(self):
        text = 'Sure! Here is the output: {"action": "respond", "message": "ok"} Hope that helps.'
        result = parse_json_response(text)
        assert result == {"action": "respond", "message": "ok"}

    def test_deeply_nested_json(self):
        text = '{"action": "tool", "parameters": {"nested": {"a": 1, "b": [1, 2, 3]}}}'
        result = parse_json_response(text)
        assert result["parameters"]["nested"]["b"] == [1, 2, 3]

    def test_empty_string_returns_none(self):
        assert parse_json_response("") is None

    def test_none_input_returns_none(self):
        assert parse_json_response(None) is None

    def test_no_json_returns_none(self):
        assert parse_json_response("just some plain text") is None

    def test_invalid_json_returns_none(self):
        assert parse_json_response("{action: respond}") is None

    def test_first_valid_json_is_returned(self):
        """Se ci sono due JSON, ritorna il primo."""
        text = '{"action": "first"} {"action": "second"}'
        result = parse_json_response(text)
        assert result["action"] == "first"


# ─────────────────────────────────────────────
# TEST: validate_output
# ─────────────────────────────────────────────

class TestValidateOutput:

    def test_valid_respond_action(self):
        data = {"action": "respond", "message": "final answer"}
        result = validate_output(data)
        assert result is not None
        assert result.action == "respond"
        assert result.message == "final answer"

    def test_valid_tool_action_with_parameters(self):
        data = {"action": "calculator", "parameters": {"expression": "3 * 4"}}
        result = validate_output(data)
        assert result is not None
        assert result.action == "calculator"
        assert result.parameters == {"expression": "3 * 4"}

    def test_action_only_is_valid(self):
        """message e parameters sono Optional — solo action è obbligatorio."""
        data = {"action": "some_tool"}
        result = validate_output(data)
        assert result is not None
        assert result.action == "some_tool"
        assert result.message is None
        assert result.parameters is None

    def test_missing_action_returns_none(self):
        data = {"message": "no action here"}
        result = validate_output(data)
        assert result is None

    def test_empty_dict_returns_none(self):
        assert validate_output({}) is None

    def test_none_input_returns_none(self):
        assert validate_output(None) is None

    def test_parameters_can_be_any_dict(self):
        data = {"action": "tool", "parameters": {"a": 1, "b": "hello", "c": [1, 2]}}
        result = validate_output(data)
        assert result is not None
        assert result.parameters["c"] == [1, 2]

    def test_extra_fields_are_ignored(self):
        """Pydantic di default ignora i campi extra."""
        data = {"action": "respond", "message": "ok", "unexpected_field": "value"}
        result = validate_output(data)
        assert result is not None
        assert result.action == "respond"


# ─────────────────────────────────────────────
# TEST: integrazione parser + validator
# ─────────────────────────────────────────────

class TestParserValidatorIntegration:

    def test_full_pipeline_respond(self):
        """Simula l'output grezzo del modello → parse → validate."""
        raw = '```json\n{"action": "respond", "message": "The result is 42"}\n```'
        parsed = parse_json_response(raw)
        validated = validate_output(parsed)
        assert validated is not None
        assert validated.action == "respond"
        assert "42" in validated.message

    def test_full_pipeline_tool_call(self):
        raw = 'Here is my decision: {"action": "calculator", "parameters": {"expression": "10 * 5"}}'
        parsed = parse_json_response(raw)
        validated = validate_output(parsed)
        assert validated is not None
        assert validated.action == "calculator"
        assert validated.parameters["expression"] == "10 * 5"

    def test_full_pipeline_invalid_json(self):
        raw = "I don't know what to do."
        parsed = parse_json_response(raw)
        assert parsed is None
        # validate_output con None ritorna None
        validated = validate_output(parsed)
        assert validated is None