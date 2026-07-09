import speech_recognition as sr


class SpeechRecognizer:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        self.microphone = sr.Microphone()

        with self.microphone as source:

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

    def listen_once(self):

        with self.microphone as source:

            audio = self.recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=10
            )

        text = self.recognizer.recognize_google(audio)
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        return text.lower().strip()

    def listen_for_phrase(self):

        with self.microphone as source:

            try:

                audio = self.recognizer.listen(
                    source,
                    timeout=1,
                    phrase_time_limit=2
                )

            except sr.WaitTimeoutError:

                return ""

        try:

            text = self.recognizer.recognize_google(audio)

            return text.lower().strip()

        except Exception:

            return ""