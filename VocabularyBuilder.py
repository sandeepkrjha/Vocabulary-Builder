import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyDictionary import PyDictionary
import sqlite3
import random

conn = sqlite3.connect('vocab.db')
cursor = conn.execute("SELECT * FROM WORDS")
dictionary = PyDictionary()

wordBank=[]
for row in cursor:
    wordBank.append(row[1])

class VocabularyBuilder(QWidget):

	def __init__(self):
		super().__init__()

		self.initDict()
	

	def initDict(self):
		self.words = QLabel('word:',self)
		self.words.move(35,17)
		self.words.resize(45,15)

		self.wordText = QLabel(self)
		self.wordText.setStyleSheet('color: green')
		self.startIndex = random.randint(0,len(wordBank))
		self.wordText.setText(wordBank[self.startIndex])
		self.wordText.setFont(QFont("Ariel", 14))
		self.wordText.resize(200,30)
		self.wordText.move(100,10)
		

		self.nextword= QPushButton('Next',self)
		self.nextword.clicked.connect(self.nextClicked)
		self.nextword.setAutoDefault(True)
		self.nextword.resize(60,30)
		self.nextword.move(210,200)

		self.meaningText= QTextEdit(self)
		self.meaningText.setDisabled(True)
		self.meaningText.setStyleSheet('color: red')
		self.meaningText.setFont(QFont("Ariel",10))
		self.scrollArea = QScrollArea(self)
		self.scrollArea.setWidget(self.meaningText)
		wordMeaning = dictionary.meaning(wordBank[self.startIndex])
		for key,value in wordMeaning.items():
			self.meaningText.setText(str(key) + ": " + str(value) + "\n")

		self.meaningText.resize(225,100)
		self.meaningText.move(100,50)
		self.scrollArea.move(100,50)
		self.scrollArea.resize(240,100)
		
		self.meaning = QPushButton('View Meaning',self)
		self.meaning.clicked.connect(self.meaningClicked)
		self.meaning.resize(100,30)
		self.meaning.move(100,160)

		self.mastered= QPushButton('Mastered',self)
		self.mastered.clicked.connect(self.masteredClicked)
		self.mastered.resize(90,30)
		self.mastered.move(210,160)
		self.mastered.setToolTip('Once mastered, this word will not appear again')

		self.exit = QPushButton('Exit',self)
		self.exit.clicked.connect(self.exitClicked)
		self.exit.resize(60,30)
		self.exit.move(140,200)

		
		self.setGeometry(350,300,400,300)
		self.setWindowTitle('Vocabulary Builder')
		self.setWindowIcon(QIcon('dictionary.png'))
		self.show()


	def nextClicked(self):
		self.meaningText.setText(" ")
		self.num = random.randint(0,len(wordBank))
		word = wordBank[self.num]
		self.wordText.setText(word)
	def exitClicked(self):
		QApplication.quit()
	def meaningClicked(self):
		wordMeaning = dictionary.meaning(wordBank[self.num])
		for key,value in wordMeaning.items():
			self.meaningText.setText(str(key) + ": " + str(value) + "\n")
		
	def masteredClicked(self):
		if QMessageBox.question(None, '', "Have you mastered this word?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No) == QMessageBox.Yes:
			wordBank.remove(wordBank[self.num])


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = VocabularyBuilder()
	sys.exit(app.exec_())

