import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QBasicTimer
import time
import threading

form_class = uic.loadUiType("mywindow.ui")[0]


def sys_exit():
    sys.exit()


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start_btn.clicked.connect(self.bench)
        self.exit_btn.clicked.connect(sys_exit)
        self.timer = QBasicTimer()
        self.step = 0
        self.pro_bar.setValue(0)
        self.log.setText('함수 초기화 중입니다.')
        self.timer.start(50, self)
    
    def bench(self):
        bench_thread = threading.Thread(target=self.bench_mark)
        bench_thread.daemon = True
        bench_thread.start()
    
    def bench_mark(self):
        daemon_start = time.time()
        debug = True
        succeed = []
        i = 8
        index = 0
        while True:
            start = time.time()
            i = i * i
            index += 1
            if debug:
                self.log.setText('{}-{}'.format(index, round(time.time() - start, 3)))
            if time.time() - start > 5:
                succeed.append(index)
                self.result.setText('{}회를 {}초만에 시행했습니다'.format(index, round(time.time() - daemon_start, 3)))
                self.score_lcd.display(index - round(time.time() - daemon_start, 2) * 100)
                return
    
    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.log.setText('함수 초기화가 완료되었습니다 시작하기를 눌러주세요')
            return

        self.step = self.step + 1
        self.pro_bar.setValue(self.step * 2)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
