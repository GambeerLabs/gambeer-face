import sys
from PyQt4 import QtGui
from gamface.gamface import MyWidget

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())