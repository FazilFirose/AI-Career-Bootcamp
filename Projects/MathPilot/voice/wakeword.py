import os
from threading import Event

import numpy as np
import speech_recognition as sr


WAKE_PHRASE = "hey math"
SAMPLE_RATE = 16000
FRAME_SIZE = 1280


class WakeWordListener:
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self._model = None
        self._model_checked = False

    def wait_for_wake_word(self, stop_event: Event) -> bool:
        model = self._load_openwakeword_model()
        if model is not None:
            return self._wait_with_openwakeword(model, stop_event)

        return self._wait_with_short_phrase_checks(stop_event)

    def _load_openwakeword_model(self):
        if self._model_checked:
            return self._model

        self._model_checked = True
        model_path = os.getenv("MATHPILOT_WAKEWORD_MODEL")
        if not model_path:
            return None

        try:
            from openwakeword.model import Model

            self._model = Model(
                wakeword_models=[model_path],
                inference_framework=os.getenv("MATHPILOT_WAKEWORD_FRAMEWORK", "onnx"),
            )
        except Exception:
            self._model = None

        return self._model

    def _wait_with_openwakeword(self, model, stop_event: Event) -> bool:
        try:
            import pyaudio
        except ImportError:
            return self._wait_with_short_phrase_checks(stop_event)

        audio = pyaudio.PyAudio()
        stream = None

        try:
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=FRAME_SIZE,
            )

            while not stop_event.is_set():
                frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
                audio_frame = np.frombuffer(frame, dtype=np.int16)
                predictions = model.predict(audio_frame)

                if _has_detection(predictions, self.threshold):
                    return True

            return False
        except OSError:
            return False
        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()
            audio.terminate()

    def _wait_with_short_phrase_checks(self, stop_event: Event) -> bool:
        recognizer = sr.Recognizer()

        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 300

        recognizer.pause_threshold = 0.8
        recognizer.non_speaking_duration = 0.5
        recognizer.phrase_threshold = 0.3
        try:
            microphone = sr.Microphone(sample_rate=SAMPLE_RATE)
        except OSError:
            return False

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.3)

            while not stop_event.is_set():
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
                except sr.WaitTimeoutError:
                    continue

                if stop_event.is_set():
                    return False

                try:
                    phrase = recognizer.recognize_google(audio).lower().strip()
                except (sr.UnknownValueError, sr.RequestError):
                    continue

                if _matches_wake_phrase(phrase):
                    return True

        return False


def _matches_wake_phrase(phrase: str) -> bool:
    normalized = " ".join(phrase.lower().split())
    return WAKE_PHRASE in normalized


def _has_detection(predictions: dict[str, float], threshold: float) -> bool:
    for score in predictions.values():
        if score >= threshold:
            return True
    return False
