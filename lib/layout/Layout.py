# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from InputForm import InputForm
from ResultView import ResultView

class Layout(QtGui.QWidget):
    
    def __init__(self):
        super(Layout, self).__init__()
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)
                        
        self.form = InputForm()
        self.result = ResultView()
        
        hbox.addWidget(self.form)
        hbox.addWidget(self.result)