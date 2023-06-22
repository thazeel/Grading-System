import os
import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, QPushButton, QMessageBox, QFileDialog, \
    QLineEdit, QVBoxLayout, QComboBox
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
import re
from nltk.stem.wordnet import WordNetLemmatizer
import enchant


class Outputbox(QWidget):
    def __init__(self, marks):
        super().__init__()
        self.msg = QMessageBox()
        self.msg.setText("The Obtained Marks are  :  " + str(marks))
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.retval = self.msg.exec_()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.w = None
        self.label_2 = None
        self.label_1 = None
        self.msgbox = None
        self.label1 = None
        self.window_width, self.window_height = 500, 300
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options = ('Get File Name', 'Get Folder Dir')

        self.combo = QComboBox()
        self.combo.addItems(self.options)
        layout.addWidget(self.combo)

        btn = QPushButton('Choose')
        btn.clicked.connect(self.launchDialog)
        layout.addWidget(btn)

    def launchDialog(self):
        option = self.options.index(self.combo.currentText())

        if option == 0:
            response = self.getFileName()
        elif option == 1:
            response = self.getDirectory()
        else:
            print('Got Nothing')
        model_answer = open(r"File Location", "r")
        model_text = model_answer.read()
        answer_text = self.read_file(response)
        model_text_list = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", model_text.lower()))
        answer_text_list = word_tokenize(re.sub(r"[^A-Za-z\d]", " ", answer_text.lower()))
        l_model = self.lemmatizer(model_text_list)
        l_student = self.lemmatizer(answer_text_list)
        l_s_model = self.no_stopwords(l_model)
        l_s_student = self.no_stopwords(l_student)
        sp_mistakes = self.misspelled(answer_text_list)
        l_s_student1 = self.synonym_equaliser(l_s_model, l_s_student)
        b = self.BoW(l_s_model, l_s_student1)
        marks = self.marking(b[0], b[1], b[2], len(sp_mistakes), len(l_s_model), 50.0, l_s_model)
        self.window3(marks)

    def window3(self, marks):
        self.w = Outputbox(marks)
        self.w.show()
        self.hide()

    def getFileName(self):
        file_filter = 'Text File (*.txt)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a text file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Text File (*.txt)'
        )
        return response[0]

    def getDirectory(self):
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select a folder'
        )
        return response

    def read_file(self, path):
        model_answer = open(path, "r")
        return model_answer.read()

    def lemmatizer(self, words):
        l = [WordNetLemmatizer().lemmatize(k) for k in words]
        return l

    def no_stopwords(self, words):
        s = []
        for k in words:
            if k not in stopwords.words("english"):
                s.append(k)
        return s

    def misspelled(self, words):
        dictionary = enchant.Dict("en_IN")
        m = []
        for i in words:
            if not dictionary.check(i):
                m.append(i)
        return m

    def syn_vector(self, obj):
        synonyms = []
        for syn in wordnet.synsets(obj):
            for i in syn.lemmas():
                synonyms.append(i.name())
        return synonyms

    def unique(self, sequence):
        seen = set()
        return [z for z in sequence if not (z in seen or seen.add(z))]

    def synonym_equaliser(self, text1, text2):
        for k in range(0, len(text2)):
            for d in self.unique(self.syn_vector(text2[k])):
                for y in text1:
                    if d == y:
                        text2[k] = y
        return text2

    def vectorize(self, set_of_words, doc_text):
        vector = []
        for i in set_of_words:
            vector.append(doc_text.count(i))
        return vector

    def BoW(self, text1, text2):
        vocab = self.unique(text1 + text2)
        bow1 = self.vectorize(vocab, text1)
        bow2 = self.vectorize(vocab, text2)
        return [vocab, bow1, bow2]

    def marking(self, vocab, bow1, bow2, num_misspelled, num_word, total_marks, text1):
        sum_large = 0
        sum_small = 0
        num_large1 = 0
        num_small1 = 0
        for i in text1:
            if len(i) > 5:
                num_large1 += 1
            else:
                num_small1 += 1
        ratio = (num_small1 + num_large1) / num_large1
        coef_large = ratio * total_marks / num_word
        coef_small = total_marks / num_word
        for i in text1:
            if len(i) > 5:
                sum_large += coef_large
            else:
                sum_small += coef_small
        total = sum_small + sum_large
        change = total_marks / total
        coef_large = change * coef_large
        coef_small = change * coef_small
        student_mark = 0
        for i in range(len(vocab)):
            if bow1[i] > 0:
                if len(vocab[i]) > 5:
                    student_mark += bow2[i] * coef_large
                else:
                    student_mark += bow2[i] * coef_small
        student_mark = student_mark - (num_misspelled / num_word) * 3
        return student_mark


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None
        self.label = None
        self.combo = None
        self.options = None
        self.msgBox = None
        self.btn = None
        self.textbox = None
        self.label_3 = None
        self.label_2 = None
        self.label_1 = None
        self.left = 700
        self.top = 300
        self.width = 500
        self.height = 450
        self.title = "Grading Machine"
        self.GUIComponents()

    def GUIComponents(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label_1 = QLabel(self)
        self.label_1.setText("Login Page")
        self.label_1.move(200, 10)
        self.label_1.resize(300, 50)
        self.label_1.setFont(QFont("Arial", 20))

        self.label_2 = QLabel(self)
        self.label_2.setText("Username  :  Administrator")
        self.label_2.resize(250, 50)
        self.label_2.move(30, 110)
        self.label_2.setFont(QFont("Times", 10))

        self.label_3 = QLabel(self)
        self.label_3.setText("Password  :  ")
        self.label_3.move(30, 150)
        self.label_3.setFont(QFont("Times", 10))

        self.textbox = QLineEdit(self)
        self.textbox.setEchoMode(QLineEdit.Password)
        self.textbox.move(130, 150)
        self.textbox.resize(150, 30)

        self.btn = QPushButton("Login", self)
        self.btn.setGeometry(180, 200, 90, 30)

        self.btn.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        if self.textbox.text() == "school":
            return self.window2()
        else:
            self.msgBox = QMessageBox()
            self.msgBox.setIcon(QMessageBox.Critical)
            self.msgBox.setText("Wrong Password")
            self.msgBox.setWindowTitle("Error !!")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.exec()

    def window2(self):
        self.w = MyApp()
        self.w.show()
        self.hide()


app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
