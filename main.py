import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCalendarWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from naver import executeNaver
from twitter import executeTwitter

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('seyoung project')
        self.move(300, 300)
        self.resize(800, 500)

        fromCal = QCalendarWidget(self)
        fromCal.setGridVisible(True)
        fromCal.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        fromCal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        fromLabel = QLabel('시작 날짜 선택', self)
        fromLabel.setAlignment(Qt.AlignCenter)

        fromCalBox = QVBoxLayout()
        fromCalBox.addWidget(fromLabel)
        fromCalBox.addWidget(fromCal)

        toCal = QCalendarWidget(self)
        toCal.setGridVisible(True)
        toCal.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        toCal.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        toLabel = QLabel('끝 날짜 선택', self)
        toLabel.setAlignment(Qt.AlignCenter)

        toCalBox = QVBoxLayout()
        toCalBox.addWidget(toLabel);
        toCalBox.addWidget(toCal);

        calBox = QHBoxLayout()
        calBox.addLayout(fromCalBox)
        calBox.addLayout(toCalBox)

        idLabel = QLabel('아이디: ', self)
        inputField = QLineEdit(self)

        naverBtn = QPushButton('네이버', self)
        naverBtn.resize(naverBtn.sizeHint())
        naverBtn.clicked.connect(lambda: executeNaver(inputField.text(), fromCal.selectedDate().toString('yyyy.MM.dd'), toCal.selectedDate().toString('yyyy.MM.dd'))
                                    if (inputField.text() != '') \
                                    else QMessageBox.about(self, "에러", "ID가 비어있습니다"))

        twitterBtn = QPushButton('트위터', self)
        twitterBtn.resize(twitterBtn.sizeHint())
        twitterBtn.clicked.connect(lambda: executeTwitter(inputField.text(), fromCal.selectedDate().toString('yyyy.MM.dd'), toCal.selectedDate().toString('yyyy.MM.dd'))
                                    if (inputField.text() != '') \
                                    else QMessageBox.about(self, "에러", "ID가 비어있습니다"))

        inputBox = QHBoxLayout()
        inputBox.addWidget(idLabel)
        inputBox.addWidget(inputField)
        inputBox.addWidget(naverBtn)
        inputBox.addWidget(twitterBtn)

        entireBox = QVBoxLayout()
        entireBox.addLayout(calBox)
        entireBox.addLayout(inputBox)

        self.setLayout(entireBox)
        self.show()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = Window()
   sys.exit(app.exec_())