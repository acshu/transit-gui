# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QHBoxLayout
from InputForm import InputForm
from ResultView import ResultView

class Layout(QWidget):
    
    def __init__(self):
        super(Layout, self).__init__()
        hbox = QHBoxLayout()
        self.setLayout(hbox)
                        
        self.form = InputForm()
        self.result = ResultView()
        self.setObjectName('Layout')
        
        hbox.addWidget(self.form)
        hbox.addWidget(self.result)