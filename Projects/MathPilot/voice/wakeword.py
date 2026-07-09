from voice.speech import SpeechRecognizer


WAKE_WORD = "math"


class WakeWordDetector:

    def __init__(self):

        self.speech = SpeechRecognizer()

    def wait_for_wake_word(self):

        while True:

            phrase = self.speech.listen_for_phrase()

            if not phrase:
                continue

            print(f"Detected: {phrase}")

            if WAKE_WORD in phrase:

                return True