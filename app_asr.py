import pyaudio
from recorder import Recorder
from PyQt5.QtCore import QThread, pyqtSignal
from baidu_asr import baidu_asr


class AsrThread(QThread):
    do_nothing = lambda *_, **__: None

    # A signal needs to be defined on class level
    ok_signal = pyqtSignal(str)
    err_signal = pyqtSignal(dict)

    def __init__(self, on_success, on_error=print):
        super(AsrThread, self).__init__()
        self.recorder = Recorder(rate=16000, channels=1, format=pyaudio.paInt16)

        self.ok_signal.connect(on_success if on_success else AsrThread.do_nothing)
        self.err_signal.connect(on_error if on_error else AsrThread.do_nothing)

        self.run = self.do_asr

    def do_asr(self):
        pcm = self.recorder.listen()
        res = baidu_asr(pcm, 'pcm', 16000)
        if res['err_msg'] == 'success.':
            self.ok_signal.emit(' '.join(res['result']))
        else:
            self.err_signal.emit({'err_no': res['err_no'], 'err_msg': res['err_msg']})


if __name__ == '__main__':
    thread = AsrThread(print, None)
    thread.start()
