# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from ..Task import Task
from ..Logger import logger

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
        
        self._group = QtGui.QGroupBox()
        self._group.setTitle('Input parameters')
        self._group.setLayout(grid)
        vbox.addWidget(self._group)

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
        
        
        self._calculate = QtGui.QPushButton('Calculate')
        self._calculate.clicked.connect(self._onCalculate)
        vbox.addWidget(self._calculate) 
       
        self._progress = QtGui.QProgressBar()
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.hide()
        vbox.addWidget(self._progress)
        
        self._cancel = QtGui.QPushButton('Cancel')
        self._cancel.hide()
        self._cancel.clicked.connect(self._onCancel)
        vbox.addWidget(self._cancel)
        
    def _onCalculate(self):
        task = Task()
        task.event.start.connect(self._onTaskStart)
        task.event.progress.connect(self._onTaskProgress)
        task.event.result.connect(self._onTaskComplete)
        task.start()
        
    def _onTaskStart(self):
        self._calculate.hide()
        self._progress.show()
        self._progress.setValue(0)
        self._cancel.show()
        self._group.setDisabled(True)
        
    def _onTaskProgress(self, progress):
        self._progress.setValue(progress)
        
    def _onTaskComplete(self, result):
        self._calculate.show()
        self._progress.hide()
        self._progress.setValue(0)
        self._cancel.hide()
        self._group.setDisabled(False)
        
    def _onStop(self):
        print 'Stop'
        
    def _onCancel(self):
        if Task.last() :
            Task.last().stop()
            
        self._calculate.show()
        self._progress.hide()
        self._progress.setValue(0)
        self._cancel.hide()
        self._group.setDisabled(False)