import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QMessageBox,
    QWidget,
    QComboBox,
    QPlainTextEdit,
)
from PyQt5.QtGui import QIcon
import asyncio
import tools
import os
import time
import json

root_path = os.path.join(os.path.dirname(__file__))


class Text2audio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QApplication.instance().setWindowIcon(
            QIcon(os.path.join(root_path, "src", "logo.png"))
        )
        self.CharacterBox = QComboBox()
        with open(
            os.path.join(root_path, "src", "audio_type.json"), "r", encoding="utf-8"
        ) as f:
            text = json.load(f)
        self.CharacterBox.addItems(text["types"])

        self.ChangeSpeed = QComboBox()
        self.ChangeSpeed.addItems(
            [
                "-50%",
                "-40%",
                "-30%",
                "-20%",
                "-10%",
                "0%",
                "10%",
                "20%",
                "30%",
                "40%",
                "50%",
            ]
        )

        GenerButton = QPushButton("生成音频")
        exitButton = QPushButton("退出")

        exitButton.clicked.connect(self.exit_app)
        GenerButton.clicked.connect(self.t2a)

        self.textEdit = QPlainTextEdit()
        vbox = QVBoxLayout()

        vbox.addWidget(self.textEdit)
        self.textEdit.setPlaceholderText("请输入要转换的文字")

        # 创建一个 QWidget 作为中心小部件，将 vbox 设置为其布局
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.CharacterBox)
        hbox.addWidget(self.ChangeSpeed)
        hbox.addWidget(GenerButton)
        hbox.addWidget(exitButton)
        vbox.addLayout(hbox)

        self.setGeometry(650, 300, 450, 350)
        self.setWindowTitle("文字转音频1.1")

    def read_textEdit(self):
        text = self.textEdit.toPlainText()
        return text

    def select_voice(self):
        select_voice = self.CharacterBox.currentText()
        select_type = select_voice.rsplit("-", 1)[0]
        return select_type

    def output_file(self):
        download_dir = os.path.expanduser("~/Downloads")
        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        output_file = os.path.join(download_dir, "{}.mp3".format(time_now))
        return output_file

    def speed(self):
        return self.ChangeSpeed.currentText()

    def t2a(self):
        loop = asyncio.get_event_loop_policy().get_event_loop()
        try:
            loop.run_until_complete(
                tools.amain(
                    self.read_textEdit(),
                    self.select_voice(),
                    self.output_file(),
                    self.speed(),
                )
            )
            QMessageBox.information(self, "生成完成", "音频已生成{}".format(self.output_file()))
        except Exception as e:
            QMessageBox.critical(self, "生成失败", str(e))

    def exit_app(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Text2audio()
    ex.show()
    sys.exit(app.exec())
