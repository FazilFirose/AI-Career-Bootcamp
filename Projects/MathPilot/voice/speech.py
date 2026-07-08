import speech_recognition as sr


class SpeechRecognizer:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 1.0
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

    def listen(self):

        try:

            with sr.Microphone() as source:

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            text = self.recognizer.recognize_google(audio)

            return text

        except sr.WaitTimeoutError:
            raise Exception("Listening timed out.")

        except sr.UnknownValueError:
            raise Exception("Couldn't understand speech.")

        except sr.RequestError:
            raise Exception("Speech recognition service unavailable.")