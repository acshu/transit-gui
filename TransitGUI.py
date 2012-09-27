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
        self.setGeometry(300, 300, 760, 420)
        self.setWindowTitle('Transit')
        self.setWindowIcon(QtGui.QIcon(os.path.join(basedir, 'assets/icon.png'))) 

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.statusBar().showMessage('Ready')
        self.show()
        logger.info('Ready')
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = TransitGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()