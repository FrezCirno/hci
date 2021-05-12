import wave
import pyaudio
import speech_recognition as sr


class Recorder:
    CHUNK = 1024

    def __init__(self, rate=16000, channels=1, format=pyaudio.paInt16):
        self.pa = pyaudio.PyAudio()
        self.rate = rate
        self.channels = channels
        self.format = format

        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(sample_rate=rate)

    def listen(self):
        with self.mic as source:
            try:
                print("适应噪声......")
                self.recognizer.adjust_for_ambient_noise(source, 0.5)
                print("开始录音......")
                audio = self.recognizer.listen(source)
                print("录音结束")
            except Exception as ex:
                print(ex)
                return b''
        return audio.frame_data

    def __del__(self):
        self.pa.terminate()

    def record(self, time_sec, save_file=None, **kwarg):
        frames = []
        stream = self.pa.open(rate=self.rate,
                              channels=self.channels,
                              format=self.format,
                              input=True,
                              frames_per_buffer=self.CHUNK,
                              **kwarg)

        print("开始录音......")
        for i in range(self.rate * time_sec // self.CHUNK):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("录音结束")

        stream.stop_stream()
        stream.close()

        frames_data = b''.join(frames)

        if save_file != None:
            with wave.open(save_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.pa.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(frames_data)

        return frames_data


if __name__ == '__main__':
    recorder = Recorder(rate=44100, format=pyaudio.paInt32, channels=2)
    recorder.record(2, save_file='1.wav')
