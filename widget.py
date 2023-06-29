# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys


from PySide2.QtWidgets import QApplication, \
    QMainWindow, QPushButton, QTextEdit, QPlainTextEdit, QFileDialog
from PySide2.QtCore import QFile, QEvent
from PySide2.QtUiTools import QUiLoader

from PySide2 import QtCore

from PySide2.QtGui import QWheelEvent, QKeyEvent
from dialogue import Dialogue



Qt = QtCore.Qt

class Widget(QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()
        self.init_dialogue

    def init_dialogue(self):
        with open(".api_key", "r") as file:
            api_key = file.read()
        self.dialogue = Dialogue(api_key)        

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        obj = loader.load(ui_file, self)

        button_open = obj.findChild(QPushButton, 'pushButtonOpen')
        button_open.clicked.connect(self.button_open_clicked)

        button_clear = obj.findChild(QPushButton, 'pushButtonClear')
        button_clear.clicked.connect(self.button_clear_clicked)

        button_save = obj.findChild(QPushButton, 'pushButtonSave')
        button_save.clicked.connect(self.button_save_clicked)

        self.bigtext = obj.findChild(QPlainTextEdit, 'bigtext')

        self.load_text_from_file()

        # Установка eventFilter для перехвата событий колесика мыши
        self.bigtext.installEventFilter(self)

        # Флаг для отслеживания состояния зажатой клавиши CTRL
        self.ctrl_pressed = False


        self.setCentralWidget(obj)
        ui_file.close()
        return obj


    def button_save_clicked(self):
        # Открытие диалога выбора файла для сохранения
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Текстовые файлы (*.txt)")

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]

            # Получение содержимого из текстового поля
            text = self.bigtext.toPlainText()

            # Запись содержимого в выбранный файл
            with open(selected_file, 'w') as file:
                file.write(text)

    def wheelEvent(self, event: QWheelEvent):
        # Проверка, что клавиша CTRL нажата
        if event.modifiers() & QtCore.Qt.ControlModifier:
            # Получение направления вращения колесика мыши
            angle_delta = event.angleDelta().y()
            if angle_delta > 0:
                # Увеличение размера шрифта
                self.change_font_size(1)
            elif angle_delta < 0:
                # Уменьшение размера шрифта
                self.change_font_size(-1)

        super().wheelEvent(event)

    def change_font_size(self, delta):
        # Получение текущего размера шрифта
        font = self.bigtext.font()
        font_size = font.pointSize()

        # Изменение размера шрифта
        new_font_size = font_size + delta
        if new_font_size > 0:
            font.setPointSize(new_font_size)
            self.bigtext.setFont(font)

    def closeEvent(self, event):
        # Сохранение содержимого текстового поля в файле
        # при закрытии приложения
        self.save_text_to_file()

        super().closeEvent(event)

    def load_text_from_file(self):
        # Проверка наличия файла entry.txt
        if os.path.exists("entry.txt"):
            # Открытие файла entry.txt и чтение его содержимого
            with open("entry.txt", 'r') as file:
                file_content = file.read()

            # Отправка содержимого файла в текстовое поле
            self.bigtext.setPlainText(file_content)

    def save_text_to_file(self):
        # Получение содержимого текстового поля
        text = self.bigtext.toPlainText()

        # Сохранение содержимого в файле entry.txt
        with open("entry.txt", 'w') as file:
            file.write(text)

    def button_open_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Текстовые файлы (*.txt);;Все файлы (*)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]

            # Открытие выбранного файла и чтение его содержимого
            with open(selected_file, 'r') as file:
                file_content = file.read()

            # Отправка содержимого файла в текстовое поле
            self.bigtext.setPlainText(file_content)

    def button_clear_clicked(self):
        self.bigtext.setPlainText("")


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    # sys.argv += ['-platform', ]

    app = QApplication(sys.argv)
    # app.setStyle('')

    widget = Widget()
    widget.resize(700, 400)
    widget.show()
    # widget.setGeometry(100, 100, 700, 500)
    sys.exit(app.exec_())
