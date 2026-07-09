import threading

from voice.wakeword import WakeWordDetector
from voice.speech import SpeechRecognizer
import time

from voice.beep import activation_beep

class VoiceController:

    def __init__(self, on_question, on_status):

     self.on_question = on_question

     self.on_status = on_status

     self.detector = WakeWordDetector()

     self.speech = SpeechRecognizer()

     self.running = False

     self.thread = None

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

    def stop(self):

        self.running = False

    def _run(self):

     while self.running:

        self.on_status("Waiting for 'Hey Math'...")

        self.detector.wait_for_wake_word()

        if not self.running:
            break

        activation_beep()

        self.on_status("🎤 Listening...")

        time.sleep(0.15)

        try:

            question = self.speech.listen_once()

            if question:

                self.on_status("🧠 Thinking...")

                self.on_question(question)

        except Exception as e:

            print(e)