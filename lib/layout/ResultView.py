# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from numpy import arange, sin, cos, pi, linspace, radians
from scipy.interpolate import spline
from transit import transit

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
    
    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(1, 1, 1)
        #self.axes.spines['right'].set_color('none')
        #self.axes.spines['top'].set_color('none')
        #self.axes.yaxis.set_ticks_position('left')
        #self.axes.xaxis.set_ticks_position('bottom')
        #self.axes.autoscale_view(tight=True)
        #fig.canvas
        #self.axes.hold(False)
        
        matplotlib.rcParams.update({'font.size': 10})
        bgColor = str(QtGui.QPalette().color(QtGui.QPalette.Active, QtGui.QPalette.Window).name())
        fig.set_facecolor(bgColor)
        fig.set_edgecolor(bgColor)
        
        A=0.0343            #semimajor axis
        Rs=A/6.05           #Stelar radius
        Rp=Rs*0.15808       #Planetary radius
        Tp=1786.00          #Planet Temperature
        Ts=6200.00          #Stellar Temperature
        i=radians(89.987)   #Inclination
        u=0.3652            #Darkenning coefficient
        
        predictionX, predictionY = transit(A,Rs,Rp,Tp,Ts,i,u, 1)
        
        A=0.0483            #semimajor axis
        Rs=A/6.05           #Stelar radius
        Rp=Rs*0.08808       #Planetary radius
        Tp=50.00            #Planet Temperature
        Ts=12000.00         #Stellar Temperature
        i=radians(89.987)   #Inclination
        u=0.3652            #Darkenning coefficient
        observationX, observationY = transit(A,Rs,Rp,Tp,Ts,i,u, 1)

        # Smoothing        
        #predictionXS = linspace(predictionX.min(), predictionX.max(), 300)
        #predictionYS = spline(predictionX, predictionY, predictionXS)
        
        #self.axes.plot(predictionXS, predictionYS, label='Prediction Smooth')
        self.axes.plot(predictionX, predictionY, label='Prediction')
        self.axes.plot(observationX, observationY, linestyle='--', color='r', label='Observation')
        self.axes.legend()
        self.axes.set_xlabel('Phase')
        self.axes.set_ylabel('Magnitude')
        self.axes.set_title('A=0.666, Rs=0.55, Rp=0.001, Ts=5000, Tp=50, i=33')

        FigureCanvas.__init__(self, fig)
        #self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
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
