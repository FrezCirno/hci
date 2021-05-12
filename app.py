import sys
import difflib
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, QTimer, pyqtSlot
from app_ui import Ui_Dialog
from app_asr import AsrThread
import app_function


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


class myWindow(QtWidgets.QDialog):
    def __init__(self):
        super(myWindow, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.asr_thread = AsrThread(self.do_sth, self.on_err)

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
        self.asr_thread = AsrThread(self.do_sth, self.on_err)
        self.start_asr()

    @pyqtSlot()
    def start_asr(self):
        self.timer.stop()
        self.ui.movie.start()
        self.ui.label_6.setText('Listening...')
        self.asr_thread.start()

    def do_sth(self, text):
        self.ui.movie.stop()
        self.ui.movie.jumpToFrame(0)
        self.ui.label_6.setText(text or 'Pardon?')

        if '播放音乐' in text or '来点音乐' in text:
            app_function.play_music()
        elif '编辑文本' in text or '编辑文件' in text or '打开记事本' in text:
            app_function.open_file()
        elif '打开浏览器' in text:
            app_function.open_browser()
        elif '打开微信' in text:
            app_function.open_wechat()
        elif '搜索' in text:
            try:
                keyword = text[text.index('搜索') + 2:]
                app_function.search(keyword)
            except:
                pass

        self.timer.start()

    def on_err(self, err):
        self.timer.start()
        self.ui.movie.stop()
        self.ui.movie.jumpToFrame(0)
        self.ui.label_6.setText('Pardon?')
        print(err)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    instance = myWindow()
    instance.show()
    sys.exit(app.exec())
