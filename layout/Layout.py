# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from InputForm import InputForm

class Layout(QtGui.QWidget):
    
    def __init__(self):
        super(Layout, self).__init__()
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)
                        
        self.form = InputForm()
        self.result = ResultView()
        
        hbox.addWidget(self.form)
        hbox.addWidget(self.result)
        
        
class ResultView(QtGui.QTabWidget):
    
    def __init__(self):
        super(ResultView, self).__init__()
        
        self.plot = ResultPlot()
        self.addTab(self.plot, 'Plot')
        
        tabTable = QtGui.QTableWidget()
        self.addTab(tabTable, 'Result table')
        
class ResultPlot(QtGui.QWidget):
    
    def __init__(self):
        super(ResultPlot, self).__init__()
        vbox = QtGui.QVBoxLayout()
        
        self.image = QtGui.QLabel()
        vbox.addWidget(self.image)

        self.toolbar = QtGui.QHBoxLayout()
        self.toolbar.setAlignment(QtCore.Qt.AlignRight)

        self.toolbar_png = QtGui.QPushButton('Save PNG')
        self.toolbar_png.clicked.connect(self.onSavePNG)
        
        self.toolbar.addWidget(self.toolbar_png)
        
        vbox.addLayout(self.toolbar)
        self.setLayout(vbox)
        
    def onSavePNG(self):
        print "Save PNG"