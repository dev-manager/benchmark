import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import random
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
    
    def bench(self):
        bench_thread = threading.Thread(target=self.bench_mark)
        bench_thread.daemon = True
        bench_thread.start()
    
    def bench_mark(self):
        daemon_start = time.time()
        debug = True
        succeed = []
        i = random.randint(5, 9)
        index = 0
        while True:
            start = time.time()
            i = i * i
            index += 1
            if debug:
                self.log.setText('{}-{}'.format(index, round(time.time() - start, 3)))
            if time.time() - start > 1.5:
                succeed.append(index)
                self.result.setText('{}회를 {}초만에 시행했습니다'.format(index, round(time.time() - daemon_start, 3)))
                self.score_lcd.display(index / round(time.time() - daemon_start, 2) * 100)
                return


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
