# -*- coding: utf-8 -*-

"""
Transit GUI

Transit callculator GUI

author: Anatoli Vladev
email: avladev@gmail.com
"""

import sys, os
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/config/"
from PyQt4.QtGui import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QDesktopWidget, QIcon
from PyQt4.QtCore import QLocale
from lib.layout.Layout import Layout
from lib.Logger import logger
from lib.layout.InputForm import InputForm

class TransitGUI(QMainWindow):
    """
    This class handles the main application window creation
    """
    def __init__(self):
        super(TransitGUI, self).__init__()
        logger.info('Running Transit')
       
        self.setLocale(QLocale(QLocale.C))
        logger.info('Init UI')
        self.setCentralWidget(Layout())
        self.setGeometry(200, 200, 1024, 600)
        self.setWindowTitle('Transit')
        self.setWindowIcon(QIcon('assets/icon.png')) 

        self.init_menu()

        frame_geometry = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())

        self.statusBar().showMessage('Ready')
        self.show()
        logger.info('Ready')
        
    def init_menu(self):
        """
        Creates application menu
        """
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        
        mopen = QAction('&Open...', self)
        mopen.setShortcut('Ctrl+O')
        mopen.setStatusTip('Open input parameters file')
        mopen.triggered.connect(self.on_open)
        
        msave = QAction('&Save as...', self)
        msave.setShortcut('Ctrl+S')
        msave.setStatusTip('Save input parameters to file')
        msave.triggered.connect(self.on_save)

        mexit = QAction('&Quit', self)
        mexit.setShortcut('Ctrl+Q')
        mexit.setStatusTip('Quit application')
        mexit.triggered.connect(self.close)
        
        file_menu.addAction(mopen)
        file_menu.addAction(msave)
        file_menu.addSeparator()
        file_menu.addAction(mexit)
    
    def on_open(self):
        """
        Opens file browser when File -> Open ... is clicked
        """
        try:
            filename = str(QFileDialog.getOpenFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().loadParams(filename)
        except Exception:
            QMessageBox.warning(self, "Error", "Error reading ini file!")
    
    def on_save(self):
        """
        Opens file browser when File -> Save ... is clicked
        """
        try:
            filename = str(QFileDialog.getSaveFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().saveParams(filename)
        except Exception:
            QMessageBox.warning(self, "Error", "Error saving ini file!")
    
    @staticmethod
    def closeEvent(cls):
        """
        Handles closing of the app
        Saves session settings
        """
        InputForm.instance().saveParams("./config/last-session.ini")
        
def main():
    
    app = QApplication(sys.argv)
    transit = TransitGUI()
    transit
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()