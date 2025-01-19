from PyQt5.QtWidgets import QApplication 
from PyQt5.QtCore import*

app = QApplication([])

file = QFile("style")
file.open(QFile.ReadOnly | QFile.Text)
stream = QTextStream(file)
app.setStyleSheet(stream.readAll())
file.close()