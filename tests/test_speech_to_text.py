import pytest
import whisper
from pathlib import Path
from services.speech_to_text import SpeechToText

class DummyModel:
    def transcribe(self, audio_path):
        # Simulate whisper transcription
        return {"text": "hello world"}

@pytest.fixture(autouse=True)
def patch_whisper(monkeypatch):
    # Monkeypatch whisper.load_model to return DummyModel
    monkeypatch.setattr(whisper, 'load_model', lambda model_name: DummyModel())


def test_transcribe(tmp_path):
    # Create a dummy WAV file
    dummy_file = tmp_path / "dummy.wav"
    dummy_file.write_bytes(b"RIFF")  # Minimal WAV header

    stt = SpeechToText(model_name='base')
    text = stt.transcribe(str(dummy_file))
    assert text == "hello world"


def test_record_and_transcribe(monkeypatch):
    # Monkeypatch record and transcribe methods
    monkeypatch.setattr(SpeechToText, 'record', lambda self, duration=5.0: 'dummy.wav')
    monkeypatch.setattr(SpeechToText, 'transcribe', lambda self, path: 'test output')

    stt = SpeechToText(model_name='base')
    result = stt.record_and_transcribe(duration=1.0)
    assert result == 'test output'
