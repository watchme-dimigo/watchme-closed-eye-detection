import wave
from time import sleep
import pyaudio


class Audio():
    def __init__(self, audio_path):
        """audio_path의 wav 파일을 가지는 Audio 객체를 생성한다."""

        self.chunk = 1024
        self.player = pyaudio.PyAudio()
        self.audio_file = wave.open(audio_path, 'rb')
        # https://freesound.org/people/austin1234575/sounds/213795/ (Creative
        # Commons 0 라이센스)
        self.stream = self.player.open(
            format=self.player.get_format_from_width(
                self.audio_file.getsampwidth()),
            channels=self.audio_file.getnchannels(),
            rate=self.audio_file.getframerate(),
            output=True)

    def play(self):
        """wav 파일을 재생한다."""

        # 재생 전에 audio_file을 rewind
        self.audio_file.rewind()

        # stream을 (다시) 시작
        self.stream.start_stream()

        # 데이터를 chunk씩 받아 재생한다.
        data = self.audio_file.readframes(self.chunk)
        while data:
            self.stream.write(data)
            data = self.audio_file.readframes(self.chunk)
        self.stream.stop_stream()

    def close(self):
        """열려 있는 스트림과 파일, player를 닫는다."""

        self.stream.close()
        self.audio_file.close()
        self.player.terminate()


if __name__ == '__main__':
    # example run
    audio = Audio('./assets/beep.wav')
    audio.play()
    sleep(0.5)
    audio.play()
    audio.close()
