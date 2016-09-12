from PyQt4 import QtCore, QtGui
 
class ImageWidget(QtGui.QWidget):
    def __init__(self, imagePath, text,parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QtGui.QPixmap(imagePath)
        self.text=text
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.picture)
        painter.setPen(QtCore.Qt.red)
        painter.setFont(QtGui.QFont("Arial", 7))
        painter.drawText(self.rect(),QtCore.Qt.AlignCenter, self.text)
