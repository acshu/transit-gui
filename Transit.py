# -*- coding: utf-8 -*-

"""
Transit GUI

Transit callculator GUI

author: Anatoli Vladev
email: avladev@gmail.com
"""

import sys
import os

from lib.Layout import Layout
from lib.Layout import InputForm
from lib.Structures import Global
from lib.Utils import logger


os.environ['MPLCONFIGDIR'] = os.getcwd() + "/config/"
from PyQt4.QtGui import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QDesktopWidget, QIcon
from PyQt4.QtCore import QLocale


class TransitGUI(QMainWindow):
    """
    This class handles the main application window creation
    """
    def __init__(self):
        super(TransitGUI, self).__init__()
        logger.info('Running Transit')

        Global.init()
       
        self.setLocale(QLocale(QLocale.C))
        logger.info('Init UI')
        self.setCentralWidget(Layout())
        screen_width = 800
        screen_height = 550

        if QApplication.desktop().screenGeometry().width() >= 900:
            screen_width = 900

        self.setGeometry(0, 0, screen_width, screen_height)

        self.setWindowTitle('TAC-maker 1.0.1')
        self.setWindowIcon(QIcon('assets/icon.png')) 

        self.init_menu()

        frame_geometry = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center)
        self.move(frame_geometry.topLeft())
        #self.showMaximized()

        self.statusBar().showMessage('Ready')
        self.show()
        logger.info('Ready')
        
    def init_menu(self):
        """
        Creates application menu
        """
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        
        action_open = QAction('&Open...', self)
        action_open.setShortcut('Ctrl+O')
        action_open.setStatusTip('Open input parameters file')
        action_open.triggered.connect(self.on_open)
        
        action_save = QAction('&Save as...', self)
        action_save.setShortcut('Ctrl+S')
        action_save.setStatusTip('Save input parameters to file')
        action_save.triggered.connect(self.on_save)

        action_exit = QAction('&Quit', self)
        action_exit.setShortcut('Ctrl+Q')
        action_exit.setStatusTip('Quit application')
        action_exit.triggered.connect(self.close)
        
        file_menu.addAction(action_open)
        file_menu.addAction(action_save)
        file_menu.addSeparator()
        file_menu.addAction(action_exit)
    
    def on_open(self):
        """
        Opens file browser when File -> Open ... is clicked
        """
        try:
            filename = str(QFileDialog.getOpenFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().load_params(filename)
        except Exception:
            QMessageBox.warning(self, "Error", "Error reading ini file!\nError: " + str(sys.exc_info()[1]))
    
    def on_save(self):
        """
        Opens file browser when File -> Save ... is clicked
        """
        try:
            filename = str(QFileDialog.getSaveFileName(self, 'Open file', directory="./data", filter="INI (*.ini);;All files (*.*)"))
            InputForm.instance().save_params(filename)
        except Exception:
            QMessageBox.warning(self, "Error", "Error saving ini file!\nError: " + str(sys.exc_info()[1]))
    
    @staticmethod
    def closeEvent(cls):
        """
        Handles closing of the app
        Saves session settings
        """
        InputForm.instance().save_params("./config/last-session.ini")

        folder = './config/temp'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e


def main():
    
    app = QApplication(sys.argv)
    transit = TransitGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()