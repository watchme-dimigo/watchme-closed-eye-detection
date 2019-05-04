import wave
from time import sleep
import pyaudio

class Audio():
    def __init__(self, audio_path):
        self.chunk = 1024
        self.player = pyaudio.PyAudio()
        self.audio_file = wave.open(audio_path, 'rb')
            # https://freesound.org/people/austin1234575/sounds/213795/ (Creative Commons 0 라이센스)
        self.stream = self.player.open(
            format=self.player.get_format_from_width(
                self.audio_file.getsampwidth()),
            channels=self.audio_file.getnchannels(),
            rate=self.audio_file.getframerate(),
            output=True)

    def play(self):
        self.audio_file.rewind()
        self.stream.start_stream()
        data = self.audio_file.readframes(self.chunk)
        while data:
            self.stream.write(data)
            data = self.audio_file.readframes(self.chunk)
        self.stream.stop_stream()

    def close(self):
        self.stream.close()
        self.player.terminate()


audio = Audio('./assets/beep.wav')
audio.play()
sleep(0.5)
audio.play()
audio.close()
