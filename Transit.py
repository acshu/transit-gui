# -*- coding: utf-8 -*-

"""
Transit GUI

Transit callculator GUI

author: Anatoli Vladev
email: avladev@gmail.com
last edited: September 2012
"""

import sys, os
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/config/"
from PyQt4.QtGui import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QIcon, QDesktopWidget
from PyQt4.QtCore import QLocale
from lib.layout.Layout import Layout
from lib.Logger import logger
from lib.layout.InputForm import InputForm

if getattr(sys, 'frozen', None):
     basedir = sys._MEIPASS
else:
     basedir = os.path.dirname(__file__)


class TransitGUI(QMainWindow):
    
    def __init__(self):
        super(TransitGUI, self).__init__()
        logger.info('Running Transit')
        logger.info('Base dir: ' + str(basedir))
        self.initUI()
        
    def initUI(self):
        self.setLocale(QLocale(QLocale.C))
        logger.info('Init UI')
        self.setCentralWidget(Layout())
        self.setGeometry(300, 300, 800, 450)
        self.setWindowTitle('Transit')
        #self.setWindowIcon(QIcon('assets/icon.png')) 

        self.initMenu()

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.statusBar().showMessage('Ready')
        self.show()
        logger.info('Ready')
        
    def initMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        
        mopen = QAction('&Open...', self)
        mopen.setShortcut('Ctrl+O')
        mopen.setStatusTip('Open input parameters file')
        mopen.triggered.connect(self.onOpen)
        
        msave = QAction('&Save as...', self)
        msave.setShortcut('Ctrl+S')
        msave.setStatusTip('Save input parameters to file')
        msave.triggered.connect(self.onSave)

        mexit = QAction('&Quit', self)
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
            filename = str(QFileDialog.getOpenFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().loadParams(filename)
        except:
            QMessageBox.warning(self, "Error", "Error reading ini file!")
    
    def onSave(self):
        try:
            filename = str(QFileDialog.getSaveFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().saveParams(filename)
        except:
            QMessageBox.warning(self, "Error", "Error saving ini file!")
    
    def closeEvent(self, event):
        InputForm.instance().saveParams("./config/last-session.ini")
        event.accept()
        
def main():
    
    app = QApplication(sys.argv)
    ex = TransitGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()