# -*- coding: utf-8 -*-

from PyQt4.QtGui import QLabel, QCheckBox, QFileDialog, QDoubleSpinBox, QWidget, QPushButton, QMessageBox, QVBoxLayout, QGridLayout, QGroupBox, QProgressBar, QComboBox
from PyQt4.QtCore import Qt, QString
from ..Task import Task
from ResultView import Plot, ResidualPlot
from ConfigParser import ConfigParser
from os.path import exists
from copy import copy
import sys, os
from ..Task import TaskImporter

class InputForm(QWidget):

    __instance = None
    
    SUN_RADIUS = 6.955*10**8
    JUPITER_RADIUS = 6.9173*10**7
    AU = 149597870691.0
    
    @staticmethod
    def instance():
        return InputForm.__instance;

    def __init__(self):
        if InputForm.__instance == None :
            InputForm.__instance = self
            
        super(InputForm, self).__init__()
        
        self._changeFromSignal = False
        self.filename = ''

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0,0,0,0)
                                        
        self.setLayout(self.vbox)
        self.setFixedWidth(290)
                        
        self.grid = QGridLayout()        
        self.grid.setAlignment(Qt.AlignTop)
        self.grid.setColumnStretch(1,1)
        
        self._group = QGroupBox()
        self._group.setTitle('Input parameters')
        self._group.setLayout(self.grid)
        self.vbox.addWidget(self._group)

        # Semi-major axis
        self.smaLabel = QLabel('Semi-major axis:')
        self.smaValue = CustomDoubleSpinBox()
        self.smaValue.setObjectName('smaValue')
        self.smaValue.setRange(0, 9999)
        self.smaValue.setSingleStep(0.01)
        self.smaValue.setDecimals(10)
        self.smaValue.setAccelerated(True)
        self.smaValue.setValue(0.0171000000) # 0.037100
        self.smaUnits = QLabel('AU')

        self.grid.addWidget(self.smaLabel, 1, 0)
        self.grid.addWidget(self.smaValue, 1, 1)
        self.grid.addWidget(self.smaUnits, 1, 2)
        
        # Stellar radius
        self.srLabel = QLabel('Stellar radius:')
        self.srValue = CustomDoubleSpinBox()
        self.srrValue = CustomDoubleSpinBox()
        
        self.srValue.valueChanged.connect(self._onSRChange)
        self.srrValue.valueChanged.connect(self._onSRRChange)
        
        self.srValue.setRange(0, 9999999999)
        self.srValue.setSingleStep(0.0001)
        self.srValue.setDecimals(10)
        self.srValue.setAccelerated(True)
        self.srValue.setValue(0.00364026905)
        self.srUnits = QLabel('AU')
        
        self.grid.addWidget(self.srLabel, 2, 0)
        self.grid.addWidget(self.srValue, 2, 1)
        self.grid.addWidget(self.srUnits, 2, 2)
        
        self.srrValue.setRange(0, 9999999999)
        self.srrValue.setSingleStep(0.01)
        self.srrValue.setDecimals(10)
        self.srrValue.setAccelerated(True)
        self.srrUnits = QLabel('R<small>sun</small>')
        
        self.grid.addWidget(self.srrValue, 3, 1)
        self.grid.addWidget(self.srrUnits, 3, 2)
        
        # Planet radius
        self.prLabel = QLabel('Planet radius:')
        self.prValue = CustomDoubleSpinBox()
        self.prrValue = CustomDoubleSpinBox()
        
        self.prValue.valueChanged.connect(self._onPRChange)
        self.prrValue.valueChanged.connect(self._onPRRChange)
        
        self.prValue.setRange(0, 9999)
        self.prValue.setSingleStep(0.01)
        self.prValue.setDecimals(10)
        self.prValue.setAccelerated(True)
        self.prValue.setValue(0.0005847123) # 0.00050471226
        self.prUnits = QLabel('AU')
        
        self.grid.addWidget(self.prLabel, 4, 0)
        self.grid.addWidget(self.prValue, 4, 1)
        self.grid.addWidget(self.prUnits, 4, 2)
        
        self.prrValue.setRange(0, 9999999999)
        self.prrValue.setSingleStep(0.01)
        self.prrValue.setDecimals(10)
        self.prrValue.setAccelerated(True)
        self.prrUnits = QLabel('R<small>jup</small>')
        
        self.grid.addWidget(self.prrValue, 5, 1)
        self.grid.addWidget(self.prrUnits, 5, 2)
        
                
        # Stellar temperature
        self.stLabel = QLabel('Stellar temperature:')
        self.stValue = CustomDoubleSpinBox()
        self.stValue.setRange(0, 99999)
        self.stValue.setSingleStep(1)
        self.stValue.setDecimals(0)
        self.stValue.setAccelerated(True)
        self.stValue.setValue(4675)
        self.stUnits = QLabel('K')
        
        self.grid.addWidget(self.stLabel, 6, 0)
        self.grid.addWidget(self.stValue, 6, 1)
        self.grid.addWidget(self.stUnits, 6, 2)
        
        # Planet temperature
        self.ptLabel = QLabel('Planet temperature:')
        self.ptValue = CustomDoubleSpinBox()
        self.ptValue.setRange(0, 99999)
        self.ptValue.setSingleStep(1)
        self.ptValue.setDecimals(0)
        self.ptValue.setAccelerated(True)
        self.ptValue.setValue(1300)
        self.ptUnits = QLabel('K')
        
        self.grid.addWidget(self.ptLabel, 7, 0)
        self.grid.addWidget(self.ptValue, 7, 1)
        self.grid.addWidget(self.ptUnits, 7, 2)
        
        # Inclination
        self.inLabel = QLabel('Inclination:')
        self.inValue = CustomDoubleSpinBox()
        self.inValue.setRange(0, 90)
        self.inValue.setSingleStep(0.01)
        self.inValue.setDecimals(10)
        self.inValue.setAccelerated(True)
        self.inValue.setValue(90) # 86.80
        self.inUnits = QLabel('Deg')
        
        
        self.grid.addWidget(self.inLabel, 8, 0)
        self.grid.addWidget(self.inValue, 8, 1)
        self.grid.addWidget(self.inUnits, 8, 2)
        
        # Darkening law
        self.dklLabel = QLabel('Darkening law:')
        self.dklValue = QComboBox()
        self.dklValue.addItem('Linear', 'linear')
        self.dklValue.addItem('Quadratic', 'quadratic')
        self.dklValue.addItem('Square root', 'squareroot')
        self.dklValue.addItem('Logarithmic', 'logarithmic')
        self.dklUnits = QLabel('')
        

        self.grid.addWidget(self.dklLabel, 9, 0)
        self.grid.addWidget(self.dklValue, 9, 1)
        self.grid.addWidget(self.dklUnits, 9, 2)
        
        # Darkening coefficient 1
        self.dk1Label = QLabel('Darkening coefficient 1:')
        self.dk1Value = CustomDoubleSpinBox()
        self.dk1Units = QLabel('')
        self.dk1Value.setRange(0, 1)
        self.dk1Value.setSingleStep(0.01)
        self.dk1Value.setDecimals(10)
        self.dk1Value.setAccelerated(True)
        self.dk1Value.setValue(0.2)

        self.grid.addWidget(self.dk1Label, 10, 0)
        self.grid.addWidget(self.dk1Value, 10, 1)
        self.grid.addWidget(self.dk1Units, 10, 2)
        
        # Darkening coefficient 2
        self.dk2Label = QLabel('Darkening coefficient 2:')
        self.dk2Value = CustomDoubleSpinBox()
        self.dk2Units = QLabel('')
        self.dk2Value.setRange(0, 1)
        self.dk2Value.setSingleStep(0.01)
        self.dk2Value.setDecimals(10)
        self.dk2Value.setAccelerated(True)
        self.dk2Value.setValue(0.2)

        self.grid.addWidget(self.dk2Label, 11, 0)
        self.grid.addWidget(self.dk2Value, 11, 1)
        self.grid.addWidget(self.dk2Units, 11, 2)
                        
        # phase end
        self.penLabel = QLabel('Phase end:')
        self.penValue = CustomDoubleSpinBox()
        self.penValue.setRange(0, 0.5)
        self.penValue.setSingleStep(0.01)
        self.penValue.setDecimals(10)
        self.penValue.setAccelerated(True)
        self.penValue.setValue(0.2)
        
        self.grid.addWidget(self.penLabel, 12, 0)
        self.grid.addWidget(self.penValue, 12, 1)
        
        # phase step
        self.pspLabel = QLabel('Phase step:')
        self.pspValue = CustomDoubleSpinBox()
        self.pspValue.setRange(0, 1)
        self.pspValue.setSingleStep(0.00001)
        self.pspValue.setDecimals(10)
        self.pspValue.setAccelerated(True)
        self.pspValue.setValue(0.0001)
        
        self.grid.addWidget(self.pspLabel, 13, 0)
        self.grid.addWidget(self.pspValue, 13, 1)

        # integration precision        
        self.pcLabel = QLabel('Integration precision 10^?:')
        self.pcValue = CustomDoubleSpinBox()
        self.pcValue.setDecimals(0)
        self.pcValue.setRange(-10, 0)
        self.pcValue.setValue(-1)
                
        self.grid.addWidget(self.pcLabel, 14, 0)
        self.grid.addWidget(self.pcValue, 14, 1)
        
        
        igrid = QGridLayout()        
        igrid.setAlignment(Qt.AlignTop)
        igrid.setColumnStretch(1,1)

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        
        self._igroup = QGroupBox()
        self._igroup.setTitle('Import settings')
        self._igroup.setLayout(igrid)
        vbox.addWidget(self._igroup)
        

        self.fnameLabel = QLabel('No file selected')
        self.fbrowse = QPushButton('Browse...')
        self.fbrowse.setFixedWidth(105)
        self.fbrowse.clicked.connect(self._onImportBrowse)
        self.fclear = QPushButton('Clear')
        self.fclear.setFixedWidth(105)
        self.fclear.clicked.connect(self._onImportClear)
        self.fclear.setHidden(True)
        igrid.addWidget(self.fnameLabel, 1, 0, 1, 0)
        igrid.addWidget(self.fbrowse, 1, 3)
        igrid.addWidget(self.fclear, 1, 3)
                
        
        self.son = QCheckBox('Convert HJD to phases')
        self.son.stateChanged.connect(self._onJDTCheck)
        igrid.addWidget(self.son, 2, 0, 1, 0)
        
        self.tzerol = QLabel('T<sub>0</sub>')
        self.tzerol.setFixedWidth(20)
        self.tzero = CustomDoubleSpinBox()
        self.tzero.setSingleStep(0.01)
        self.tzero.setDecimals(10)
        self.tzero.setAccelerated(True)
        self.tzero.setDisabled(True)
        self.tzero.setMinimum(0)
        self.tzero.setFixedWidth(230)
        self.tzero.setRange(0, sys.float_info.max)
        igrid.addWidget(self.tzerol, 3, 0)
        igrid.addWidget(self.tzero, 3, 1)
        
        self.periodl = QLabel('P')
        self.periodl.setFixedWidth(20)
        self.period = CustomDoubleSpinBox()
        self.period.setFixedWidth(230)
        self.period.setDisabled(True)
        self.period.setRange(0, sys.float_info.max)
        self.period.setDecimals(10)
        igrid.addWidget(self.periodl, 4, 0)
        igrid.addWidget(self.period, 4, 1)
        
        self.mon = QCheckBox('Convert magnitude to flux')
        self.mon.stateChanged.connect(self._onMagCheck)
        igrid.addWidget(self.mon, 5, 0, 1, 0)

        self.mmaxl = QLabel('Mag')
        self.mmax = CustomDoubleSpinBox()
        self.mmax.setSingleStep(0.01)
        self.mmax.setDecimals(10)
        self.mmax.setAccelerated(True)
        self.mmax.setDisabled(True)
        self.mmax.setMinimum(0)
        self.mmax.setFixedWidth(105)
        igrid.addWidget(self.mmaxl, 6, 0)
        igrid.addWidget(self.mmax, 6, 1)
        
        self.redraw = QPushButton("Redraw")
        self.redraw.clicked.connect(self._onRedraw)
        igrid.addWidget(self.redraw, 6,3)
        
        
        self.vbox.addWidget(self._igroup)


        self._calculate = QPushButton('Calculate')
        self._calculate.clicked.connect(self._onCalculate)
        self.vbox.addWidget(self._calculate) 
       
        self._progress = QProgressBar()
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.hide()
        self.vbox.addWidget(self._progress)
        
        self._cancel = QPushButton('Cancel')
        self._cancel.hide()
        self._cancel.clicked.connect(self._onCancel)
        self.vbox.addWidget(self._cancel)
        
        if exists("./config/last-session.ini") :
            self.loadParams("./config/last-session.ini")

        
    def _onSRChange(self, value):
        if self._changeFromSignal == False :
            self._changeFromSignal = True
            self.srrValue.setValue((value*InputForm.AU)/InputForm.SUN_RADIUS)
            self._changeFromSignal = False
            
    def _onSRRChange(self, value):
        if self._changeFromSignal == False :
            self._changeFromSignal = True
            self.srValue.setValue(value*InputForm.SUN_RADIUS/InputForm.AU)
            self._changeFromSignal = False
        
    def _onPRChange(self, value):
        if self._changeFromSignal == False :
            self._changeFromSignal = True
            self.prrValue.setValue((value*InputForm.AU)/InputForm.JUPITER_RADIUS)
            self._changeFromSignal = False
            
    def _onPRRChange(self, value):
        if self._changeFromSignal == False :
            self._changeFromSignal = True
            self.prValue.setValue(value*InputForm.JUPITER_RADIUS/InputForm.AU)
            self._changeFromSignal = False
            
    def _onJDTCheck(self, state):
        if state == Qt.Checked :
            self.tzero.setDisabled(False)
            self.period.setDisabled(False)
        else:
            self.tzero.setDisabled(True)
            self.period.setDisabled(True)
        pass
    
    def _onMagCheck(self, state):
        if state == Qt.Checked :
            self.mmax.setDisabled(False)
        else:
            self.mmax.setDisabled(True)
        pass
                        
        
    def _onImportBrowse(self):
        
        directory = "" if self.filename is None else QString(str("/").join(str(self.filename).split("/")[:-1]))
        types = TaskImporter.getFormats()
        filters = []
        
        for value in types :
            filters.append(value.upper() + " (*." + value + ")")
            
        filters.append("All files (*.*)")
        
        self.filename = QFileDialog.getOpenFileName(self, 'Open file', directory=directory, filter=";;".join(filters))
        
        self._updateFileLabel()
        
    def _onImportClear(self):
        self.filename = ''
        Plot.instance().setResult([], [])
        Plot.instance().setImport([], [])
        Plot.instance().redraw()
        ResidualPlot.instance().redraw()
        self._updateFileLabel();
        
    def _updateFileLabel(self):
        if self.filename :
            self.fnameLabel.setText(self.filename.split("/")[-1])
            self.fclear.setHidden(False)
            self.redraw.setDisabled(False)
        else:
            self.fnameLabel.setText('No file selected')
            self.fclear.setHidden(True)
            self.redraw.setDisabled(True)
        pass
            
    def _importObservation(self):
        if not self.filename :
            return
            
        try:
            result = TaskImporter.loadFile(self.filename)
            
            # convert JD time to phases
            if self.son.checkState() == Qt.Checked :
                if self.tzero.value() <= 0 :
                    QMessageBox.warning(self, "Error", 'Invalid parameter "T<sub>0</sub>"!')
                    return
                    
                if self.period.value() <= 0 :
                    QMessageBox.warning(self, "Error", 'Invalid parameter "P"!')
                    return
                    
                for (index, phase) in enumerate(result.phases):
                    result.phases[index] = (phase - self.tzero.value()) / self.period.value() % 1;
            
            
            # convert magnitude to flux
            if self.mon.checkState() == Qt.Checked :
                for (index, value) in enumerate(result.values):
                    result.values[index] = 10**(-(value - self.mmax.value())/2.5)  
                

            phases = copy(result.phases)
            values = copy(result.values)
            
            for (index, phase) in enumerate(result.phases):
                if phase > 0.5 :
                    phases[index] = phase - 1
                        
            Plot.instance().setImport(phases, values)
            Plot.instance().redraw()
            
        except:
            QMessageBox.critical(self, "Import error", "Error importing data!\nError: " + str(sys.exc_info()[1]))
            raise
            
    def _onRedraw(self):
        if not self.filename :
            QMessageBox.warning(self, "Import file", "Please import file first")
            return
        self._importObservation()
        pass
        
    def _onCalculate(self):


        self._importObservation()

        task = Task()        
        task.input.semi_major_axis = self.smaValue.value()
        task.input.star_radius = self.srValue.value()
        task.input.planet_radius = self.prValue.value()
        task.input.star_temperature = self.stValue.value()
        task.input.planet_temperature = self.ptValue.value()
        task.input.darkening_law = self.dklValue.itemData(self.dklValue.currentIndex()).toString();
        task.input.darkening_1 = self.dk1Value.value()
        task.input.darkening_2 = self.dk2Value.value()
        task.input.inclination = self.inValue.value()
        task.input.phase_start = 0
        task.input.phase_end = self.penValue.value()
        task.input.phase_step = self.pspValue.value()
        task.input.precision = 10**self.pcValue.value()
        
        if len(Plot.instance().import_phases):
            task.input.phases_injection = copy(Plot.instance().import_phases)
        
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
        self._igroup.setDisabled(True)
        
    def _onTaskProgress(self, progress):
        self._progress.setValue(progress)
        
    def _onTaskComplete(self, result):
        self._calculate.show()
        self._progress.hide()
        self._progress.setValue(0)
        self._cancel.hide()
        self._group.setDisabled(False)
        self._igroup.setDisabled(False)
        

                
        Plot.instance().setResult(result.phases, result.values)
        Plot.instance().redraw()
        ResidualPlot.instance().redraw()
        
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
        self._igroup.setDisabled(False)
        
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

        if config.has_option('input', 'darkening_law'):
            self.dklValue.setCurrentIndex(config.getint('input', 'darkening_law'))
            
        if config.has_option('input', 'darkening_1'):
            self.dk1Value.setValue(config.getfloat('input', 'darkening_1'))
            
        if config.has_option('input', 'darkening_2'):
            self.dk2Value.setValue(config.getfloat('input', 'darkening_2'))
            
        if config.has_option('input', 'phase_end'):
            self.penValue.setValue(config.getfloat('input', 'phase_end'))
            
        if config.has_option('input', 'phase_step'):
            self.pspValue.setValue(config.getfloat('input', 'phase_step'))
            
        if config.has_option('input', 'precision'):
            self.pcValue.setValue(config.getfloat('input', 'precision'))



        if config.has_option('import', 'filename') and config.get('import', 'filename') :
            if '/data/' in config.get('import', 'filename') and config.get('import', 'filename').index('/data/') == 0 :
                self.filename = os.getcwd().replace('\\', '/') + config.get('import', 'filename')
            else:
                self.filename = config.get('import', 'filename')
            
        self._updateFileLabel();

        if config.has_option('import', 'jd2phase') and config.getboolean('import', 'jd2phase') == True :
            self.son.setCheckState(Qt.Checked)
            
        if config.has_option('import', 'jd2phase_tzero') :
            self.tzero.setValue(config.getfloat('import', 'jd2phase_tzero'))
            
        if config.has_option('import', 'jd2phase_period') :
            self.period.setValue(config.getfloat('import', 'jd2phase_period'))
            
        if config.has_option('import', 'mag2flux') and config.getboolean('import', 'mag2flux') == True :
            self.mon.setCheckState(Qt.Checked)
            
        if config.has_option('import', 'mag2flux_mag') :
            self.mmax.setValue(config.getfloat('import', 'mag2flux_mag'))
            
            
    
    def saveParams(self, filename):
        config = ConfigParser()
        config.add_section('input')
        
        config.set('input', 'semi_major_axis', self.smaValue.value())
        config.set('input', 'star_radius', self.srValue.value())
        config.set('input', 'planet_radius', self.prValue.value())
        config.set('input', 'star_temperature', self.stValue.value())
        config.set('input', 'planet_temperature', self.ptValue.value())
        config.set('input', 'inclination', self.inValue.value())
        config.set('input', 'darkening_law', self.dklValue.currentIndex())
        config.set('input', 'darkening_1', self.dk1Value.value())
        config.set('input', 'darkening_2', self.dk2Value.value())
        config.set('input', 'phase_end', self.penValue.value())
        config.set('input', 'phase_step', self.pspValue.value())
        config.set('input', 'precision', self.pcValue.value())
        
        config.add_section('import')
        print self.filename
        if os.getcwd().replace('\\', '/') in str(self.filename) and str(self.filename).index(os.getcwd().replace('\\', '/')) == 0 :
            saveFilePath = str(self.filename).replace(os.getcwd().replace('\\', '/'), '')
        else:
            saveFilePath = str(self.filename)
            
        config.set('import', 'filename', saveFilePath)
        config.set('import', 'jd2phase', self.son.checkState() == Qt.Checked)
        config.set('import', 'jd2phase_tzero', self.tzero.value())
        config.set('import', 'jd2phase_period', self.period.value())
        config.set('import', 'mag2flux', self.mon.checkState() == Qt.Checked)
        config.set('import', 'mag2flux_mag', self.mmax.value())
        
        with open(filename, 'wb') as configfile:
            config.write(configfile)
        pass
    
    
class CustomDoubleSpinBox(QDoubleSpinBox):
    
    def __init__(self,parent=None,value=0):
        super(CustomDoubleSpinBox, self).__init__(parent)
        
    def textFromValue(self, value):
        result = str(QDoubleSpinBox.textFromValue(self, value))
        if result.find(".") > 0 :
            result = result.rstrip("0")
            result = result.rstrip(".")
        return result