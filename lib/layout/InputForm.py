# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from ..Task import Task, TaskInput
from ..Logger import logger
from ResultView import Plot
from ConfigParser import ConfigParser
import os

class InputForm(QtGui.QWidget):

    __instance = None
    
    @staticmethod
    def instance():
        return InputForm.__instance;

    def __init__(self):

        if InputForm.__instance == None :
            InputForm.__instance = self
            
        super(InputForm, self).__init__()

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.setContentsMargins(0,0,0,0)
                                        
        self.setLayout(self.vbox)
        self.setFixedWidth(290)
                        
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
        self.smaValue.setDecimals(10)
        self.smaValue.setAccelerated(True)
        self.smaValue.setValue(0.0171000000) # 0.037100
        self.smaUnits = QtGui.QLabel('AU')

        self.grid.addWidget(self.smaLabel, 1, 0)
        self.grid.addWidget(self.smaValue, 1, 1)
        self.grid.addWidget(self.smaUnits, 1, 2)
        
        # Stellar radius
        self.srLabel = QtGui.QLabel('Stellar radius:')
        self.srValue = QtGui.QDoubleSpinBox()
        self.srValue.setRange(0, 9999)
        self.srValue.setSingleStep(0.01)
        self.srValue.setDecimals(10)
        self.srValue.setAccelerated(True)
        self.srValue.setValue(0.00364026905)
        self.srUnits = QtGui.QLabel('AU')
        
        self.grid.addWidget(self.srLabel, 2, 0)
        self.grid.addWidget(self.srValue, 2, 1)
        self.grid.addWidget(self.srUnits, 2, 2)
        
        # Planet radius
        self.prLabel = QtGui.QLabel('Planet radius:')
        self.prValue = QtGui.QDoubleSpinBox()
        self.prValue.setRange(0, 9999)
        self.prValue.setSingleStep(0.01)
        self.prValue.setDecimals(10)
        self.prValue.setAccelerated(True)
        self.prValue.setValue(0.0005847123) # 0.00050471226
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
        self.stValue.setValue(4675)
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
        self.ptValue.setValue(1300)
        self.ptUnits = QtGui.QLabel('K')
        
        self.grid.addWidget(self.ptLabel, 5, 0)
        self.grid.addWidget(self.ptValue, 5, 1)
        self.grid.addWidget(self.ptUnits, 5, 2)
        
        # Inclination
        self.inLabel = QtGui.QLabel('Inclination:')
        self.inValue = QtGui.QDoubleSpinBox()
        self.inValue.setRange(0, 90)
        self.inValue.setSingleStep(0.01)
        self.inValue.setDecimals(10)
        self.inValue.setAccelerated(True)
        self.inValue.setValue(90) # 86.80
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
        self.dkValue.setDecimals(10)
        self.dkValue.setAccelerated(True)
        self.dkValue.setValue(0.2)

        self.grid.addWidget(self.dkLabel, 7, 0)
        self.grid.addWidget(self.dkValue, 7, 1)
        self.grid.addWidget(self.dkUnits, 7, 2)
        
        # phase start
        self.pstLabel = QtGui.QLabel('Phase start:')
        self.pstValue = QtGui.QDoubleSpinBox()
        self.pstValue.setRange(0, 1)
        self.pstValue.setSingleStep(0.01)
        self.pstValue.setDecimals(10)
        self.pstValue.setAccelerated(True)
        self.pstValue.setValue(0)
        
        self.grid.addWidget(self.pstLabel, 8, 0)
        self.grid.addWidget(self.pstValue, 8, 1)
        
        # phase end
        self.penLabel = QtGui.QLabel('Phase end:')
        self.penValue = QtGui.QDoubleSpinBox()
        self.penValue.setRange(0, 1)
        self.penValue.setSingleStep(0.01)
        self.penValue.setDecimals(10)
        self.penValue.setAccelerated(True)
        self.penValue.setValue(0.2)
        
        self.grid.addWidget(self.penLabel, 9, 0)
        self.grid.addWidget(self.penValue, 9, 1)
        
        # phase step
        self.pspLabel = QtGui.QLabel('Phase step:')
        self.pspValue = QtGui.QDoubleSpinBox()
        self.pspValue.setRange(0, 1)
        self.pspValue.setSingleStep(0.00001)
        self.pspValue.setDecimals(10)
        self.pspValue.setAccelerated(True)
        self.pspValue.setValue(0.0001)
        
        self.grid.addWidget(self.pspLabel, 10, 0)
        self.grid.addWidget(self.pspValue, 10, 1)

        # integration precision        
        self.pcLabel = QtGui.QLabel('Intgration precision 10^?:')
        self.pcValue = QtGui.QDoubleSpinBox()
        self.pcValue.setDecimals(0)
        self.pcValue.setRange(-10, 0)
        self.pcValue.setValue(-1)
                
        self.grid.addWidget(self.pcLabel, 11, 0)
        self.grid.addWidget(self.pcValue, 11, 1)
        
        
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
        
        if os.path.exists("./data/last.ini") :
            self.loadParams("./data/last.ini")
        
    def _onCalculate(self):

        task = Task()        
        task.input.semi_major_axis = self.smaValue.value()
        task.input.star_radius = self.srValue.value()
        task.input.planet_radius = self.prValue.value()
        task.input.star_temperature = self.stValue.value()
        task.input.planet_temperature = self.ptValue.value()
        task.input.darkening = self.dkValue.value()
        task.input.inclination = self.inValue.value()
        task.input.phase_start = self.pstValue.value()
        task.input.phase_end = self.penValue.value()
        task.input.phase_step = self.pspValue.value()
        task.input.precision = 10**self.pcValue.value()
        
        if len(Plot.instance().import_phases):
            task.input.phases_injection = Plot.instance().import_phases
        
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
        
    def loadParams(self, filename):
        config = ConfigParser()
        config.read(filename)
        
        if config.has_option('input', 'semi_major_axis'):
            self.smaValue.setValue(config.getfloat('input', 'semi_major_axis'))
            
        if config.has_option('input', 'star_radius'):
            self.srValue.setValue(config.getfloat('input', 'star_radius'))
            
        if config.has_option('input', 'planet_radius'):
            self.prValue.setValue(config.getfloat('input', 'planet_radius'))
            
        if config.has_option('input', 'star_temperature'):
            self.stValue.setValue(config.getfloat('input', 'star_temperature'))
            
        if config.has_option('input', 'planet_temperature'):
            self.ptValue.setValue(config.getfloat('input', 'planet_temperature'))

        if config.has_option('input', 'inclination'):
            self.inValue.setValue(config.getfloat('input', 'inclination'))            
            
        if config.has_option('input', 'darkening'):
            self.dkValue.setValue(config.getfloat('input', 'darkening'))
            
        if config.has_option('input', 'phase_start'):
            self.pstValue.setValue(config.getfloat('input', 'phase_start'))
            
        if config.has_option('input', 'phase_end'):
            self.penValue.setValue(config.getfloat('input', 'phase_end'))
            
        if config.has_option('input', 'phase_step'):
            self.pspValue.setValue(config.getfloat('input', 'phase_step'))
            
        if config.has_option('input', 'precision'):
            self.pcValue.setValue(config.getfloat('input', 'precision'))
            
    
    def saveParams(self, filename):
        config = ConfigParser()
        config.add_section('input')
        
        config.set('input', 'semi_major_axis', self.smaValue.value())
        config.set('input', 'star_radius', self.srValue.value())
        config.set('input', 'planet_radius', self.prValue.value())
        config.set('input', 'star_temperature', self.stValue.value())
        config.set('input', 'planet_temperature', self.ptValue.value())
        config.set('input', 'inclination', self.inValue.value())
        config.set('input', 'darkening', self.dkValue.value())
        config.set('input', 'phase_start', self.pstValue.value())
        config.set('input', 'phase_end', self.penValue.value())
        config.set('input', 'phase_step', self.pspValue.value())
        config.set('input', 'precision', self.pcValue.value())
        
        with open(filename, 'wb') as configfile:
            config.write(configfile)
        pass