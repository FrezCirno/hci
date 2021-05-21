from aip import AipSpeech

APP_ID = '24133290'
API_KEY = 'vhZj6fE1qrXdm5hNr0Dbkivv'
SECRET_KEY = 'KO3i9zXGQNNQG5XElOXheSRRcrd6isFc'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def baidu_asr(wave, format, rate):
    return client.asr(wave, format, rate, {
        'dev_pid': 1537,
    })


if __name__ == '__main__':
    import pyaudio
    from recorder import Recorder

    recorder = Recorder(rate=16000, channels=1, format=pyaudio.paInt16)
    res = recorder.record(3, save_file='1.wav')
    reco = baidu_asr(res, 'pcm', 16000)
    print(reco)
