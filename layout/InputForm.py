# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class InputForm(QtGui.QWidget):

    def __init__(self):
        super(InputForm, self).__init__()

        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
                                        
        self.setLayout(vbox)
        self.setFixedWidth(250)
        
        grid = QtGui.QGridLayout()        
        grid.setAlignment(QtCore.Qt.AlignTop)
        grid.setColumnStretch(1,1)
        
        self.group = QtGui.QGroupBox()
        self.group.setTitle('Input parameters')
        self.group.setLayout(grid)
        
        vbox.addWidget(self.group)

        # Semi-major axis
        smaLabel = QtGui.QLabel('Semi-major axis:')
        smaValue = QtGui.QDoubleSpinBox()
        smaUnits = QtGui.QLabel('AU')

        grid.addWidget(smaLabel, 1, 0)
        grid.addWidget(smaValue, 1, 1)
        grid.addWidget(smaUnits, 1, 2)
        
        # Stellar radius
        srLabel = QtGui.QLabel('Stellar radius:')
        srValue = QtGui.QDoubleSpinBox()
        srUnits = QtGui.QLabel('AU')
        
        grid.addWidget(srLabel, 2, 0)
        grid.addWidget(srValue, 2, 1)
        grid.addWidget(srUnits, 2, 2)
        
        # Planet radius
        prLabel = QtGui.QLabel('Planet radius:')
        prValue = QtGui.QDoubleSpinBox()
        prUnits = QtGui.QLabel('AU')
        
        grid.addWidget(prLabel, 3, 0)
        grid.addWidget(prValue, 3, 1)
        grid.addWidget(prUnits, 3, 2)
                
        # Stellar temperature
        stLabel = QtGui.QLabel('Stellar temperature:')
        stValue = QtGui.QDoubleSpinBox()
        stUnits = QtGui.QLabel('K')
        
        grid.addWidget(stLabel, 4, 0)
        grid.addWidget(stValue, 4, 1)
        grid.addWidget(stUnits, 4, 2)
        
        # Planet temperature
        ptLabel = QtGui.QLabel('Planet temperature:')
        ptValue = QtGui.QDoubleSpinBox()
        ptUnits = QtGui.QLabel('K')
        
        grid.addWidget(ptLabel, 5, 0)
        grid.addWidget(ptValue, 5, 1)
        grid.addWidget(ptUnits, 5, 2)
        
        # Inclination
        inLabel = QtGui.QLabel('Inclination:')
        inValue = QtGui.QDoubleSpinBox()
        inUnits = QtGui.QLabel('Deg')
        inValue.setMinimum( 0)
        inValue.setMaximum(90);
        
        
        grid.addWidget(inLabel, 6, 0)
        grid.addWidget(inValue, 6, 1)
        grid.addWidget(inUnits, 6, 2)
        
        # Darkening coefficient
        dkLabel = QtGui.QLabel('Darkening coefficient:')
        dkValue = QtGui.QDoubleSpinBox()
        dkUnits = QtGui.QLabel('')
        dkValue.setMinimum(0)
        dkValue.setMaximum(1);
        
        
        grid.addWidget(dkLabel, 7, 0)
        grid.addWidget(dkValue, 7, 1)
        grid.addWidget(dkUnits, 7, 2)
        
        
        self.calculate = QtGui.QPushButton('Calculate')
        self.calculate.clicked.connect(self.onCalculate)
        vbox.addWidget(self.calculate) 
       
        self.progress = QtGui.QProgressBar()
        self.progress.setValue(33)
        self.progress.setTextVisible(False)
        self.progress.hide()
        vbox.addWidget(self.progress)
        
        self.cancel = QtGui.QPushButton('Cancel')
        self.cancel.hide()
        self.cancel.clicked.connect(self.onCancel)
        vbox.addWidget(self.cancel)
        
        
    def onCalculate(self):
        self.calculate.hide()
        self.progress.show()
        self.cancel.show()
        self.group.setDisabled(True)
        
    def onCancel(self):
        self.calculate.show()
        self.progress.hide()
        self.cancel.hide()
        self.group.setDisabled(False)