# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from numpy import arange, sin, cos, pi, linspace, radians
from scipy.interpolate import spline

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
        self.plot = Plot()
        vbox.addWidget(self.plot)

        self.toolbar = QtGui.QHBoxLayout()
        self.toolbar.setAlignment(QtCore.Qt.AlignRight)

        self.toolbar_import = QtGui.QPushButton('Import')
        self.toolbar_import.clicked.connect(self.onImport)
        self.toolbar.addWidget(self.toolbar_import)

        self.toolbar_exportplot = QtGui.QPushButton('Export')
        self.toolbar_exportplot.clicked.connect(self.onExportPlot)
        self.toolbar.addWidget(self.toolbar_exportplot)
        
        vbox.addLayout(self.toolbar)
        self.setLayout(vbox)
        
    def onExportPlot(self):
        # show export dialog
        dlg = ExportPlotDialog()
        dlg.exec_()
        print "Export"
        
    def onImport(self):
        dlg = ImportDialog()
        dlg.exec_()
        print "Import"
        
class Plot(FigureCanvas):

    __instance = None
    
    import_phases = []
    import_values = []
    
    result_phases = []
    result_values = []
    
    def __init__(self):
        if Plot.__instance is None :
            Plot.__instance = self
        else:
            raise Exception("Plot is singleton!")
        
        bgColor = str(QtGui.QPalette().color(QtGui.QPalette.Active, QtGui.QPalette.Window).name())
        matplotlib.rcParams.update({'font.size': 10})        
                    
        self.figure = Figure(facecolor=bgColor, edgecolor=bgColor)
        super(Plot, self).__init__(self.figure)
        
        
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #self.axes.spines['right'].set_color('none')
        #self.axes.spines['top'].set_color('none')
        #self.axes.yaxis.set_ticks_position('left')
        #self.axes.xaxis.set_ticks_position('bottom')
        #self.axes.autoscale_view(tight=True)
        #fig.canvas
        #self.axes.hold(False)
                                       
        self.updateGeometry()
        
    @staticmethod
    def instance():
        return Plot.__instance
        
    def clear(self):
        self.figure.clear()
        self.draw()
        
    def setResult(self, phases, values):
        self.result_phases = phases
        self.result_values = values
                
    def setImport(self, phases, values):
        self.import_phases = phases
        self.import_values = values
        
    def redraw(self):
        self.clear()
        
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.grid(True)
        self.axes.set_xlabel('Phase')
        self.axes.set_ylabel('Magnitude')        
        
        if len(self.result_phases):
            self.axes.plot(self.result_phases, self.result_values, color='b', label="Prediction")
        
        if len(self.import_phases):
            self.aximport = self.figure.add_subplot(1,1,1)
            self.aximport.plot(self.import_phases, self.import_values, linestyle='--', color='r', label='Observation')
                
        self.draw()
        
        
class ImportDialog(QtGui.QDialog):
    
    def __init__(self):
        super(ImportDialog, self).__init__()
        self.setWindowTitle('Import...')
        self.setWindowIcon(QtGui.QIcon('assets/import.png'))
        self.resize(400, 160)
        
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        fgroup = QtGui.QGroupBox('Choose file')
        fgroup.setFixedHeight(60)
        fhbox = QtGui.QHBoxLayout()
        fgroup.setLayout(fhbox)
        label = QtGui.QLabel('No file selected')
        fhbox.addWidget(label)
        fbrowse = QtGui.QPushButton('Browse...')
        fbrowse.setFixedWidth(80)
        fhbox.addWidget(fbrowse)
        vbox.addWidget(fgroup)

        sgroup = QtGui.QGroupBox('Settings')
        sgroup.setFixedHeight(60)
        sgrid = QtGui.QGridLayout()
        sgrid.setAlignment(QtCore.Qt.AlignTop)
        sgroup.setLayout(sgrid)
        ssepLabel = QtGui.QLabel('Separator:')
        ssepValue = QtGui.QLineEdit(';')
        sgrid.addWidget(ssepLabel, 1, 0)
        sgrid.addWidget(ssepValue, 1, 1)

        sescLabel = QtGui.QLabel('Quote char:')
        sescValue = QtGui.QLineEdit('"')
        sgrid.addWidget(sescLabel, 1, 2)
        sgrid.addWidget(sescValue, 1, 3)
        
        shedLabel = QtGui.QLabel('Skip first line:')
        shedCheck = QtGui.QCheckBox()
        sgrid.addWidget(shedLabel, 1, 4)
        sgrid.addWidget(shedCheck, 1, 5)    
        
        vbox.addWidget(sgroup)

        bhbox = QtGui.QHBoxLayout()
        bhbox.setAlignment(QtCore.Qt.AlignRight)
        bimport = QtGui.QPushButton('Import')
        bimport.clicked.connect(self.onImport)
        bhbox.addWidget(bimport)
        bcancel = QtGui.QPushButton('Cancel')
        bcancel.clicked.connect(self.close)
        bhbox.addWidget(bcancel)
        
        vbox.addLayout(bhbox)                
        self.setLayout(vbox)
        
    def onImport(self):
        print 'import'
        
class ExportPlotDialog(QtGui.QDialog):
    
    def __init__(self):
        super(ExportPlotDialog, self).__init__()
        self.setWindowTitle('Export plot')
        self.setWindowIcon(QtGui.QIcon('assets/export.png'))
        self.resize(400, 200)
        
        
class ExportDatDialog(QtGui.QFileDialog):
    
    def __init__(self):
        super(ExportDatDialog, self).__init__()
        self.setWindowTitle('Export DAT')
        self.setWindowIcon(QtGui.QIcon('assets/export.png'))
        self.resize(500, 400)
        self.setFileMode(QtGui.QFileDialog.AnyFile)
        fname = self.getSaveFileName(directory='export.dat', filter='DAT (*.dat);;')
        print fname
