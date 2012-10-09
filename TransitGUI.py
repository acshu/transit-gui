# -*- coding: utf-8 -*-

"""
Transit GUI

Transit callculator GUI

author: Anatoli Vladev
email: avladev@gmail.com
last edited: September 2012
"""

import sys, os
from PyQt4 import QtGui, QtCore
from lib.layout.Layout import Layout
from lib.Logger import logger
from lib.layout.InputForm import InputForm

if getattr(sys, 'frozen', None):
     basedir = sys._MEIPASS
else:
     basedir = os.path.dirname(__file__)


class TransitGUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(TransitGUI, self).__init__()
        logger.info('Running Transit')
        self.initUI()
        
    def initUI(self):
        self.setLocale(QtCore.QLocale(QtCore.QLocale.C))
        logger.info('Init UI')
        self.setCentralWidget(Layout())
        self.setGeometry(300, 300, 800, 450)
        self.setWindowTitle('Transit')
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'assets/icon.png'))) 

        self.initMenu()

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.statusBar().showMessage('Ready')
        self.show()
        logger.info('Ready')
        
    def initMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        
        mopen = QtGui.QAction('&Open...', self)
        mopen.setShortcut('Ctrl+O')
        mopen.setStatusTip('Open input parameters file')
        mopen.triggered.connect(self.onOpen)
        
        msave = QtGui.QAction('&Save as...', self)
        msave.setShortcut('Ctrl+S')
        msave.setStatusTip('Save input parameters to file')
        msave.triggered.connect(self.onSave)

        mexit = QtGui.QAction('&Quit', self)
        mexit.setShortcut('Ctrl+Q')
        mexit.setStatusTip('Quit application')
        mexit.triggered.connect(self.close)
        
        fileMenu.addAction(mopen)
        fileMenu.addAction(msave)
        fileMenu.addSeparator()
        fileMenu.addAction(mexit)
        pass
    
    def onOpen(self):
        try:
            filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().loadParams(filename)
        except:
            QtGui.QMessageBox.warning(self, "Error", "Error reading ini file!")
    
    def onSave(self):
        try:
            filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().saveParams(filename)
        except:
            QtGui.QMessageBox.warning(self, "Error", "Error saving ini file!")
    
    def closeEvent(self, event):
        InputForm.instance().saveParams("./data/last.ini")
        event.accept()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = TransitGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()