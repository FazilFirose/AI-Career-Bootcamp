import threading
from collections.abc import Callable

from engine import process_question
from voice.speech import listen
from voice.tts import speak
from voice.wakeword import WakeWordListener


StatusCallback = Callable[[str], None]
QuestionCallback = Callable[[str], None]
AnswerCallback = Callable[[str], None]
ErrorCallback = Callable[[str], None]


class VoiceController:
    def __init__(
        self,
        on_status: StatusCallback,
        on_question: QuestionCallback,
        on_answer: AnswerCallback,
        on_error: ErrorCallback,
    ):
        self.on_status = on_status
        self.on_question = on_question
        self.on_answer = on_answer
        self.on_error = on_error
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._wakeword_listener = WakeWordListener()

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def _run(self) -> None:
        self.on_status("Waiting for wake word...")

        while not self._stop_event.is_set():
            detected = self._wakeword_listener.wait_for_wake_word(self._stop_event)

            if not detected or self._stop_event.is_set():
                break

            try:
                self.on_status("Wake word detected")
                self.on_status("Listening...")
                question = listen()
                self.on_question(question)

                answer = process_question(question, status_callback=self.on_status)
                self.on_answer(answer)

                self.on_status("Speaking...")
                speak(answer)
                self.on_status("Waiting for wake word...")
            except RuntimeError as exc:
                self.on_error(str(exc))
                if not self._stop_event.is_set():
                    self.on_status("Waiting for wake word...")

    @staticmethod
    def spoken_answer(answer: str) -> str:
        marker = "Answer:"
        if marker not in answer:
            return answer.strip()

        return answer.split(marker, maxsplit=1)[1].strip()
