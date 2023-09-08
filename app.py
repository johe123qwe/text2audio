"""
文字转音频
"""

import sys
from PyQt6.QtWidgets import (QMainWindow, QPushButton, QHBoxLayout, 
                             QVBoxLayout, QApplication, QTextEdit,
                             QMessageBox, QWidget, QComboBox)
import asyncio
import tools
import os
import time
import json


download_dir = os.path.expanduser("~/Downloads")
print(download_dir)

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.CharacterBox = QComboBox()
        with open('src/audio_type.json', "r", encoding="utf-8") as f:
                text = json.load(f)
        self.CharacterBox.addItems(text['types'])

        GenerButton = QPushButton("生成音频")
        exitButton = QPushButton("退出")

        exitButton.clicked.connect(self.exit_app)
        GenerButton.clicked.connect(self.t2a)

        self.textEdit = QTextEdit()
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
        hbox.addWidget(GenerButton)
        hbox.addWidget(exitButton)
        vbox.addLayout(hbox)

        self.setGeometry(650, 300, 450, 350)
        self.setWindowTitle('文字转音频1.0')

    def read_textEdit(self):
        text = self.textEdit.toPlainText()
        print(text)
        return text

    def select_voice(self):
        select_voice = self.CharacterBox.currentText()
        select_type = select_voice.rsplit('-', 1)[0]
        return select_type

    def output_file(self):
        time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
        output_file = os.path.join(download_dir, '{}.mp3'.format(time_now))
        return output_file

    def t2a(self):
        loop = asyncio.get_event_loop_policy().get_event_loop()
        try:
            loop.run_until_complete(tools.amain(self.read_textEdit(), self.select_voice(), self.output_file()))
            QMessageBox.information(self, "生成完成", "音频已生成{}".format(self.output_file()))
        except Exception as e:
            QMessageBox.critical(self, "生成失败", str(e))
        finally:
            loop.close()

    def exit_app(self):
        sys.exit()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()