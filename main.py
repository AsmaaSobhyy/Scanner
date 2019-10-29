import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from scanner import scanner
import sys


#-----------------------caling scanner function ----------------------------------
def runScanner():
    file_name = sys.argv[1] if len(sys.argv)>1 else 'tiny.txt'
    obj = scanner()
    obj.scan(file_name)
    obj.output()

#-----------------------------------initialize a window-----------------------
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        #-----------------------input text area-----------------------------
        self.b = QPlainTextEdit(self)
        self.b.resize(460,500)
        self.b.textChanged.connect(self.getText)
        self.b.setPlaceholderText("please write code here.")
        #---------------------output text area--------------------------------
        self.out = QPlainTextEdit(self)
        self.out.resize(450,500)
        self.out.move(470,0)
        self.out.textChanged.connect(self.getText)
        self.out.setReadOnly(True)
        self.out.setStyleSheet( """QPlainTextEdit {background-color: #333;color: #fff;}""")
        
        self.initUI()
        
        
    def initUI(self):
        #----------------main window-----------------
        self.setGeometry(50, 50, 900, 600)
        self.setWindowTitle('scanner')  
        #-----------------scan button-----------------
        self.scan = QPushButton('scan',self)
        self.scan.move(420,520)
        self.scan.resize(90,40)
        self.scan.clicked.connect(self.run)     
        #----------------info button-----------------
        self.info = QPushButton('',self)
        self.info.setIcon(QIcon("./Question_Mark-512.png"))
        self.info.setStyleSheet(( """QPushButton {background-color: #fff;color: #fff;border-radius:50%;}"""))
        self.info.setIconSize(QSize(45,45))
        self.info.move(850,520)
        self.info.resize(45,45)
        self.info.clicked.connect(self.getInfo)     
    
        self.show()

#--------------------------------write txt from gui to 'tiny.txt'-------------------------------------
    def getText(self):
        f= open("tiny.txt","w+")
        f.write(self.b.document().toPlainText())
        f.close()

#-------------------------------write the output into gui------------------------------------------    
    def write(self):
        f=open("output.txt", "r")
        content =f.read()
        self.out.document().setPlainText(content)
        f.close()

#--------------------------------run scanner function----------------------------------------
    def run(self):
        runScanner()
        self.write()

#-------------------------------pop up msg from info.txt-----------------------------------------------------
    def getInfo(self):
        f=open("info.txt", "r")
        content =f.read()
        self.msg=QMessageBox.about(self, "about", content)
        f.close()

#-----------------------empty files before closing-----------------------------------------------
    def closeEvent(self, event):
        f=open("output.txt", "w+")
        content =f.write("")
        f.close()
        f=open("tiny.txt", "w+")
        content =f.write("")
        f.close()
        
        


    



    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w =  Example()
    

    sys.exit(app.exec_())