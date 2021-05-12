# Lab1: Automatic Speech Recognition

# Run the Program

* You can run the program by running `app.py` in PyCharm or other IDEs
* Or running by command in the root directory: `python app.py`

## Dependency

| Package           | Version      |
|-------------------|--------------|
| baidu-aip         | 2.2.18.0     |
| PyAudio           | 0.2.11       |
| PyQt5             | 5.15.2       |
| pywin32           | 300          |
| qt5-tools         | 5.15.2.1.0.1 |
| SpeechRecognition | 3.8.1        |

```shell
pip install -r requirements.txt
```

# Developing

## Install development tools

```shell
pip install -r requirements.txt
```

## Design your UI

```shell
pyqt5-tools designer app_ui.ui

(...Drawing the UI...)

pyuic5 app_ui.ui -o app_ui.py
```

Now we get a `app_ui.py` file contains a class called `Ui_Dialog`.

## Code the logic

Basic Framework

```py
class myWindow(QDialog):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    instance = myWindow()
    instance.show()
    sys.exit(app.exec())
```

Then add the `ASR`, `Timer`, `Funtions`, etc. into it.
