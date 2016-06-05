import sys
import os

from PyQt4 import QtCore, QtGui, uic


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class MyWidget(QtGui.QMainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()        
        
        #timer para controle de medicao de tempo 
        self.timerTime = QtCore.QTimer(self)
        self.count = QtCore.QTime()
        
        #timer para controle de medicao de temperatura
        self.timerTemperature = QtCore.QTimer(self)
        self.contador = 0
        
        uic.loadUi('layout.ui', self)
                
        QtCore.QObject.connect(self.buttonStart, QtCore.SIGNAL(_fromUtf8("clicked()")), self.startCount)
        QtCore.QObject.connect(self.buttonStop, QtCore.SIGNAL(_fromUtf8("clicked()")), self.stopCount)
        QtCore.QObject.connect(self.buttonOn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.onEngine)
        QtCore.QObject.connect(self.buttonOff, QtCore.SIGNAL(_fromUtf8("clicked()")), self.offEngine)
        QtCore.QObject.connect(self.buttonClear, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clear)        
        
        #QtCore.QObject.connect(self.timerTime, QtCore.SIGNAL(_fromUtf8("timeout()")), self.updateTime)
        self.timerTime.timeout.connect(self.updateTime)
        
        self.startMeasureTemperature()
        
        self.printDisplayLCD()        
        self.show()
    
    def startMeasureTemperature(self):
        self.timerTemperature.timeout.connect(self.updateTemperature)
        self.timerTemperature.start(1000)
     
    def startCount(self):
        self.count= QtCore.QTime.fromString(self.lineEditTime.text(), "hh:mm:ss");  
        self.timerTime.start(1000)
        self.printDisplayLCD()
    
    def stopCount(self):
        self.timerTime.stop()
        
    def onEngine(self):
        print "liga motor"
        
    def offEngine(self):
        print "desliga motor"
        
    def updateTime(self): 
        if (self.count.hour() == 0 and self.count.minute() == 0 and self.count.second() == 0) :
            self.timerTime.stop()
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (3, 1000))
        else:                    
            self.count = self.count.addSecs(-1)
                                   
        self.printDisplayLCD()
    
    def updateTemperature(self):
        print("medindo tempratura ", self.contador)
        self.contador += 1
    
    def printDisplayLCD(self):        
        h = self.count.hour()
        m = self.count.minute()
        s = self.count.second()        
        time = ("{0}:{1}:{2}".format(h,m,s))
        self.lcdNumberTime.display(time)
    
    def clear(self):
        self.lineEditTime.clear()
        self.lineEditTempSup.clear()
        self.lineEditTempInf.clear()
                    
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())