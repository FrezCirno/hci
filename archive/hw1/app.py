import sys
import time
import pyaudio
from recorder import Recorder
from baidu_asr import baidu_asr
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, QTimer, pyqtSlot, pyqtSignal
from app_ui import Ui_Dialog
import app_function


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

    def run(self):
        pcm = self.recorder.listen()
        res = baidu_asr(pcm, 'pcm', 16000)
        if res['err_msg'] == 'success.':
            self.ok_signal.emit(' '.join(res['result']))
        else:
            self.err_signal.emit({'err_no': res['err_no'], 'err_msg': res['err_msg']})


class myWindow(QtWidgets.QDialog):
    def __init__(self):
        super(myWindow, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.movie = QtGui.QMovie("assets/voice.gif")
        self.ui.movie.frameChanged.connect(lambda: self.ui.voiceFig.setIcon(QtGui.QIcon(self.ui.movie.currentPixmap())))

        self.asr_thread = AsrThread(self.on_succ, self.on_err)

        '''自动触发识别'''
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.start_asr)
        self.timer.start()
        self.start_asr()

    @pyqtSlot()
    def on_voiceFig_clicked(self):
        '''手动触发识别'''
        self.asr_thread.terminate()
        self.asr_thread = AsrThread(self.on_succ, self.on_err)
        self.start_asr()

    @pyqtSlot()
    def start_asr(self):
        self.timer.stop()
        self.asr_thread.start()
        time.sleep(0.5)
        self.ui.movie.start()
        self.ui.status.setText('我在听....')

    def on_succ(self, text):
        self.ui.movie.stop()
        self.ui.movie.jumpToFrame(0)
        self.ui.status.setText(text)
        print(text)

        try:
            if '播放音乐' in text or '来点音乐' in text:
                app_function.play_music(self)
            elif '编辑文本' in text or '编辑文件' in text or '打开记事本' in text:
                app_function.open_program(self, '记事本')
            elif '打开' in text:
                keyword = text[text.index('打开') + 2:]
                app_function.open_program(self, keyword)
            elif '启动' in text:
                keyword = text[text.index('启动') + 2:]
                app_function.open_program(self, keyword)
            elif '搜索' in text:
                keyword = text[text.index('搜索') + 2:]
                if '百度' in text:
                    app_function.search(self, keyword, 'baidu')
                elif '谷歌' in text:
                    app_function.search(self, keyword, 'google')
                else:
                    app_function.search(self, keyword, 'bing')
            elif '汇率' in text:
                keyword1 = text[text.index('从') + 1:text.index('到')]
                keyword2 = text[text.index('到') + 1:text.index('的汇率')]
                app_function.exchange_rate(self, keyword1, keyword2)
            elif '几点' in text or '几分' in text or '时间' in text:
                app_function.report_time(self)
            elif '哪年' in text or '几月' in text or '几号' in text or '周几' in text or '星期几' in text or '日期' in text:
                app_function.report_date(self)
            elif 'hello' in text or '你好' in text:
                self.ui.status.setText('你好，我是Yuni')
            else:
                self.ui.status.setText('什么？我没有听清....')
        except:
            self.ui.status.setText('什么？我没有听清....')

        self.timer.start()

    def on_err(self, err):
        self.timer.start()
        self.ui.movie.stop()
        self.ui.movie.jumpToFrame(0)
        self.ui.status.setText('什么？我没有听清....')
        print(err)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    instance = myWindow()
    instance.show()
    sys.exit(app.exec())
