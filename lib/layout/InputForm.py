# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from ..Task import Task, TaskInput
from ..Logger import logger
from ResultView import Plot

class InputForm(QtGui.QWidget):

    def __init__(self):
        super(InputForm, self).__init__()

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.setContentsMargins(0,0,0,0)
                                        
        self.setLayout(self.vbox)
        self.setFixedWidth(250)
        
        self.grid = QtGui.QGridLayout()        
        self.grid.setAlignment(QtCore.Qt.AlignTop)
        self.grid.setColumnStretch(1,1)
        
        self._group = QtGui.QGroupBox()
        self._group.setTitle('Input parameters')
        self._group.setLayout(self.grid)
        self.vbox.addWidget(self._group)

        # Semi-major axis
        self.smaLabel = QtGui.QLabel('Semi-major axis:')
        self.smaValue = QtGui.QDoubleSpinBox()
        self.smaValue.setObjectName('smaValue')
        self.smaValue.setRange(0, 9999)
        self.smaValue.setSingleStep(0.01)
        self.smaValue.setDecimals(6)
        self.smaValue.setAccelerated(True)
        self.smaValue.setValue(10)
        self.smaUnits = QtGui.QLabel('AU')

        self.grid.addWidget(self.smaLabel, 1, 0)
        self.grid.addWidget(self.smaValue, 1, 1)
        self.grid.addWidget(self.smaUnits, 1, 2)
        
        # Stellar radius
        self.srLabel = QtGui.QLabel('Stellar radius:')
        self.srValue = QtGui.QDoubleSpinBox()
        self.srValue.setRange(0, 9999)
        self.srValue.setSingleStep(0.01)
        self.srValue.setDecimals(6)
        self.srValue.setAccelerated(True)
        self.srValue.setValue(1)
        self.srUnits = QtGui.QLabel('AU')
        
        self.grid.addWidget(self.srLabel, 2, 0)
        self.grid.addWidget(self.srValue, 2, 1)
        self.grid.addWidget(self.srUnits, 2, 2)
        
        # Planet radius
        self.prLabel = QtGui.QLabel('Planet radius:')
        self.prValue = QtGui.QDoubleSpinBox()
        self.prValue.setRange(0, 9999)
        self.prValue.setSingleStep(0.01)
        self.prValue.setDecimals(6)
        self.prValue.setAccelerated(True)
        self.prValue.setValue(0.1)
        self.prUnits = QtGui.QLabel('AU')
        
        self.grid.addWidget(self.prLabel, 3, 0)
        self.grid.addWidget(self.prValue, 3, 1)
        self.grid.addWidget(self.prUnits, 3, 2)
                
        # Stellar temperature
        self.stLabel = QtGui.QLabel('Stellar temperature:')
        self.stValue = QtGui.QDoubleSpinBox()
        self.stValue.setRange(0, 99999)
        self.stValue.setSingleStep(1)
        self.stValue.setDecimals(0)
        self.stValue.setAccelerated(True)
        self.stValue.setValue(8000)
        self.stUnits = QtGui.QLabel('K')
        
        self.grid.addWidget(self.stLabel, 4, 0)
        self.grid.addWidget(self.stValue, 4, 1)
        self.grid.addWidget(self.stUnits, 4, 2)
        
        # Planet temperature
        self.ptLabel = QtGui.QLabel('Planet temperature:')
        self.ptValue = QtGui.QDoubleSpinBox()
        self.ptValue.setRange(0, 99999)
        self.ptValue.setSingleStep(1)
        self.ptValue.setDecimals(0)
        self.ptValue.setAccelerated(True)
        self.ptValue.setValue(80)
        self.ptUnits = QtGui.QLabel('K')
        
        self.grid.addWidget(self.ptLabel, 5, 0)
        self.grid.addWidget(self.ptValue, 5, 1)
        self.grid.addWidget(self.ptUnits, 5, 2)
        
        # Inclination
        self.inLabel = QtGui.QLabel('Inclination:')
        self.inValue = QtGui.QDoubleSpinBox()
        self.inValue.setRange(0, 90)
        self.inValue.setSingleStep(0.01)
        self.inValue.setDecimals(6)
        self.inValue.setAccelerated(True)
        self.inValue.setValue(90)
        self.inUnits = QtGui.QLabel('Deg')
        
        
        self.grid.addWidget(self.inLabel, 6, 0)
        self.grid.addWidget(self.inValue, 6, 1)
        self.grid.addWidget(self.inUnits, 6, 2)
        
        # Darkening coefficient
        self.dkLabel = QtGui.QLabel('Darkening coefficient:')
        self.dkValue = QtGui.QDoubleSpinBox()
        self.dkUnits = QtGui.QLabel('')
        self.dkValue.setRange(0, 1)
        self.dkValue.setSingleStep(0.01)
        self.dkValue.setDecimals(6)
        self.dkValue.setAccelerated(True)
        self.dkValue.setValue(0.2)

        
        
        self.grid.addWidget(self.dkLabel, 7, 0)
        self.grid.addWidget(self.dkValue, 7, 1)
        self.grid.addWidget(self.dkUnits, 7, 2)
        
        
        self._calculate = QtGui.QPushButton('Calculate')
        self._calculate.clicked.connect(self._onCalculate)
        self.vbox.addWidget(self._calculate) 
       
        self._progress = QtGui.QProgressBar()
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.hide()
        self.vbox.addWidget(self._progress)
        
        self._cancel = QtGui.QPushButton('Cancel')
        self._cancel.hide()
        self._cancel.clicked.connect(self._onCancel)
        self.vbox.addWidget(self._cancel)
        
    def _onCalculate(self):

        task = Task()        
        task.input.semi_major_axis = self.smaValue.value()
        task.input.star_radius = self.srValue.value()
        task.input.planet_radius = self.prValue.value()
        task.input.star_temperature = self.stValue.value()
        task.input.planet_temperature = self.ptValue.value()
        task.input.darkening = self.dkValue.value()
        task.input.inclination = self.inValue.value()
        task.input.phase_start = 0.0
        task.input.phase_end = 0.2
        task.input.phase_step = 0.001
        
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
        Plot.instance().setResult(result.phases, result.values)
        Plot.instance().redraw()
        
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