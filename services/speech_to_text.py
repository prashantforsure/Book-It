import whisper
import sounddevice as sd
import numpy as np
import tempfile
import wave

class SpeechToText:
    
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def record(self, duration: float = 5.0, fs: int = 16000) -> str:
        
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        audio = np.squeeze(audio)

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        with wave.open(tmp.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes((audio * 32767).astype(np.int16).tobytes())
        return tmp.name

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes the given WAV file to text.
        """
        result = self.model.transcribe(audio_path)
        return result.get("text", "")

    def record_and_transcribe(self, duration: float = 5.0) -> str:
        """
        Helper to record audio then immediately transcribe.
        """
        path = self.record(duration)
        return self.transcribe(path)
