import asyncio
import os
import tempfile

import edge_tts
import pygame


class Speaker:

    def __init__(self):

        pygame.mixer.init()

        self.voice = "en-US-AriaNeural"

    def speak(self, text):

        asyncio.run(self._speak(text))

    async def _speak(self, text):

        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

        try:

            communicate = edge_tts.Communicate(
                str(text),
                self.voice
            )

            await communicate.save(path)

            pygame.mixer.music.load(path)

            pygame.mixer.music.play()

            
            while pygame.mixer.music.get_busy():

              await asyncio.sleep(0.1)

        finally:

            try:
                pygame.mixer.music.unload()
            except Exception:
                pass

            if os.path.exists(path):
                os.remove(path)