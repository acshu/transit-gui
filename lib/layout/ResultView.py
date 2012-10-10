# -*- coding: utf-8 -*-

from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QGroupBox, QLabel, QIcon, QDialog, QWidget, QTableWidget, QTabWidget, QPushButton, QPalette, QSizePolicy
from PyQt4.QtCore import Qt, QString
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
from ..Task import TaskImporter

class ResultView(QTabWidget):
    
    def __init__(self):
        super(ResultView, self).__init__()
        
        self.plot = ResultPlot()
        self.addTab(self.plot, 'Plot')
        
        tabTable = QTableWidget()
        self.addTab(tabTable, 'Result table')
        
class ResultPlot(QWidget):
    
    def __init__(self):
        super(ResultPlot, self).__init__()
        vbox = QVBoxLayout()
        self.plot = Plot()
        vbox.addWidget(self.plot)

        self.toolbar = QHBoxLayout()
        self.toolbar.setAlignment(Qt.AlignRight)

        self.toolbar_import = QPushButton('Import')
        self.toolbar_import.clicked.connect(self.onImport)
        self.toolbar.addWidget(self.toolbar_import)

        self.toolbar_exportplot = QPushButton('Export')
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
        
        bgColor = str(QPalette().color(QPalette.Active, QPalette.Window).name())
        rcParams.update({'font.size': 10})        
                    
        self.figure = Figure(facecolor=bgColor, edgecolor=bgColor)
        self.figure.hold(False)
        super(Plot, self).__init__(self.figure)
        
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
            self.axes.scatter(self.import_phases, self.import_values, s=0.1, color='r', label='Observation')
                
        self.draw()
        
        
class ImportDialog(QDialog):

    filename = None
    
    def __init__(self):
        super(ImportDialog, self).__init__()
        self.setWindowTitle('Import...')
        self.setWindowIcon(QIcon('assets/import.png'))
        self.resize(400, 100)
        
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        fgroup = QGroupBox('Choose file')
        fgroup.setFixedHeight(60)
        fhbox = QHBoxLayout()
        fgroup.setLayout(fhbox)
        self.fnameLabel = QLabel('No file selected')
        fhbox.addWidget(self.fnameLabel)
        fbrowse = QPushButton('Browse...')
        fbrowse.setFixedWidth(80)
        fbrowse.clicked.connect(self._onBrowse)
        fhbox.addWidget(fbrowse)
        vbox.addWidget(fgroup)
        
        bhbox = QHBoxLayout()
        bhbox.setAlignment(Qt.AlignRight)
        bimport = QPushButton('Import')
        bimport.clicked.connect(self._onImport)
        bhbox.addWidget(bimport)
        bcancel = QPushButton('Cancel')
        bcancel.clicked.connect(self.close)
        bhbox.addWidget(bcancel)
        
        vbox.addLayout(bhbox)                
        self.setLayout(vbox)
        
    def _onBrowse(self):
        directory = "" if self.filename is None else QString("/").join(self.filename.split("/")[:-1])
        types = TaskImporter.getFormats()
        filters = []
        
        for value in types :
            filters.append(value.upper() + " (*." + value + ")")
            
        filters.append("All files (*.*)")
        
        filename = QFileDialog.getOpenFileName(self, 'Open file', directory=directory, filter=";;".join(filters))
        
        if filename :
            self.filename = filename
            self.fnameLabel.setText(filename.split("/")[-1])
        else:
            self.fnameLabel.setText('No file selected')
        
        
    def _onImport(self):
        if self.filename is None :
            QMessageBox.warning(self, "Error", "Choose file!")
            return
        try:
            result = TaskImporter.loadFile(self.filename)
            Plot.instance().setImport(result.phases, result.values)
            Plot.instance().redraw()
        except:
            QMessageBox.critical(self, "Import error", "Error importing data!")
            
       
        self.close()
        
class ExportPlotDialog(QDialog):
    
    def __init__(self):
        super(ExportPlotDialog, self).__init__()
        self.setWindowTitle('Export plot')
        self.setWindowIcon(QIcon('assets/export.png'))
        self.resize(400, 200)
        
        
class ExportDatDialog(QFileDialog):
    
    def __init__(self):
        super(ExportDatDialog, self).__init__()
        self.setWindowTitle('Export DAT')
        self.setWindowIcon(QIcon('assets/export.png'))
        self.resize(500, 400)
        self.setFileMode(QFileDialog.AnyFile)
        fname = self.getSaveFileName(directory='export.dat', filter='DAT (*.dat);;')
        print fname
