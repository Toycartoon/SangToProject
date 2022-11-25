import sys, random, re, time
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget
from PyQt5 import uic
from PyQt5.QtCore import QThread
from Backend import word_check, choose_word, check_dueum


form = uic.loadUiType("systemUI.ui")[0]


class Worker(QThread):

    def __init__(self, parent):
        super(Worker, self).__init__(parent)
        self.parent = parent

    def run(self):
        w = self.parent.TextEditor.text()
        self.parent.TextEditor.clear()

        if self.parent.status:
            if w == "":
                self.parent.System_m.setText("[System] : 패배하셨습니다.. \n Enter를 눌러 다시 시작해주세요.")
                self.parent.status = False
                return
            if w[0] != self.parent.s:
                to_compare = check_dueum(self.parent.s)
                if to_compare is None or to_compare != w[0]:
                    self.parent.System_m.setText(f"[System] : \"{self.parent.s}\"로 시작하는 단어를 입력해주세요")
                    return
            elif len(w) == 1:
                self.parent.System_m.setText("[System] : 한 단어는 입력하실 수 없습니다.")
                return
            elif re.search("[^가-힣]", w):
                self.parent.System_m.setText("[System] : 모든 단어는 가-힣 사이의 한글로만 이루어져야합니다.")
                return
            r_w, r_e = word_check(w, self.parent.used)

            if r_w != w:
                self.parent.System_m.setText(r_e)
                return
            else:
                self.parent.Word.setText(r_w)
                self.parent.Description.setText(r_e)
                self.parent.System_m.setText("[System] : 잠시만 기다려주세요..")
                time.sleep(1)
                self.parent.user_turn = False
                result, word = choose_word(w[len(w) - 1], self.parent.used)

                if result:
                    self.parent.Word.setText(word[0])
                    self.parent.Description.setText(word[1])
                    self.parent.user_turn = True
                    self.parent.s = word[0][len(word[0]) - 1]
                    self.parent.System_m.setText(f"[System] : \"{self.parent.s}\"로 시작하는 단어를 입력해주세요")
                else:
                    self.parent.System_m.setText("[System] : 승리하셨습니다! \n Enter를 눌러 다시 시작해주세요.")
                    self.parent.status = False
        else:
            self.parent.Word.clear()
            self.parent.Description.clear()
            self.parent.status = True
            self.parent.s = random.choice(["가", "나", "다", "라", "마"])   # 배열 안에 넣고 싶은 단어를 넣어주세요
            self.parent.System_m.setText(f"[System] : 다음 단어로 끝말잇기를 해주세요 \"{self.parent.s}\" "
                                  f"\n 단어가 더 이상 생각나지 않으신다면 Enter를 입력해주세요.")


class SangToGUI(QWidget, form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.used = []
        self.user_turn = True
        self.status = True
        self.s = random.choice(["가", "나", "다", "라", "마"])   # 배열 안에 넣고 싶은 단어를 넣어주세요
        self.System_m.setText(f"[System] : 다음 단어로 끝말잇기를 해주세요 \"{self.s}\" "
                              f"\n 단어가 더 이상 생각나지 않으신다면 Enter를 입력해주세요.")
        self.sendButton.clicked.connect(self.sendMessage)
        self.TextEditor.returnPressed.connect(self.sendMessage)
        self.Description.setWordWrap(True)
        self.setCenter()
        self.show()

    def setCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sendMessage(self):
        self.worker = Worker(self)
        self.worker.start()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = SangToGUI()
   sys.exit(app.exec_())


