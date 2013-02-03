# -*- coding: utf-8 -*-

import sys
import csv
from copy import copy
from PyQt4.QtGui import QHBoxLayout, QVBoxLayout, QGridLayout, QCheckBox, QAbstractItemView, QDoubleSpinBox, QFileDialog, QMessageBox, QGroupBox, QLabel, QIcon, QDialog, QWidget, QTableWidget, QTableWidgetItem, QTabWidget, QPushButton, QPalette, QSizePolicy
from PyQt4.QtCore import Qt, QString, QLocale
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
from ..Task import TaskImporter

class ResultView(QTabWidget):
    
    def __init__(self):
        super(ResultView, self).__init__()
        
        self.plot = ResultPlot()
        self.addTab(self.plot, 'Plot')
        
        self.tabTable = ResultTable()
        self.addTab(self.tabTable, 'Result table')
        
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

        rightPhases = copy(phases);
        rightPhases.reverse()
        rightValues = copy(values);
        rightValues.reverse()
        
        for (index, phase) in enumerate(rightPhases):
            rightPhases[index] =-phase;
            
        self.result_phases = rightPhases + phases
        self.result_values = rightValues + values
                
    def setImport(self, phases, values):
        self.import_phases = phases
        self.import_values = values
        
    def redraw(self):
        ResultTable.instance().setData(self.result_phases, self.result_values, self.import_phases, self.import_values)
        self.clear()
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.grid(True)
        self.axes.set_xlabel('Phase')
        self.axes.set_ylabel('Flux')
        
        if len(self.result_phases):
            self.axes.plot(self.result_phases, self.result_values, color='b', label="Prediction")
        
        if len(self.import_phases):
            self.axes.scatter(self.import_phases, self.import_values, s=0.1, color='r', label='Observation')
                
        self.draw()
        
        
class ImportDialog(QDialog):

    filename = None
    
    def __init__(self):
        super(ImportDialog, self).__init__()
        self.setLocale(QLocale(QLocale.C))
        self.setWindowTitle('Import...')
        #self.setWindowIcon(QIcon('assets/import.png'))
        self.resize(200, 100)
        
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
        
        grid = QGridLayout()        
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        
        _group = QGroupBox()
        _group.setTitle('Import settings')
        _group.setLayout(grid)
        vbox.addWidget(_group)

        self.mon = QCheckBox('Convert magnitude to flux')
        grid.addWidget(self.mon, 1, 0, 1, 0)        
        
        self.son = QCheckBox('Convert JD to phases')
        self.son.stateChanged.connect(self._onJDTCheck)
        grid.addWidget(self.son, 2, 0, 1, 0)
        
        self.tzerol = QLabel('T<sub>0</sub>')
        self.tzerol.setFixedWidth(60)
        self.tzero = CustomDoubleSpinBox()
        self.tzero.setSingleStep(0.01)
        self.tzero.setDecimals(10)
        self.tzero.setAccelerated(True)
        self.tzero.setDisabled(True)
        self.tzero.setMinimum(0)
        self.tzero.setFixedWidth(120)
        self.tzero.setRange(0, sys.float_info.max)
        grid.addWidget(self.tzerol, 4, 0)
        grid.addWidget(self.tzero, 4, 1)
        
        self.periodl = QLabel('P')
        self.periodl.setFixedWidth(60)
        self.period = CustomDoubleSpinBox()
        self.period.setFixedWidth(120)
        self.period.setDisabled(True)
        self.period.setRange(0, sys.float_info.max)
        self.period.setDecimals(10)
        grid.addWidget(self.periodl, 5, 0)
        grid.addWidget(self.period, 5, 1)
        
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
        
    def _onJDTCheck(self, state):
        if state == Qt.Checked :
            self.tzero.setDisabled(False)
            self.period.setDisabled(False)
        else:
            self.tzero.setDisabled(True)
            self.period.setDisabled(True)
        pass
                        
        
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
                    
                    if result.phases[index] > 0.5 :
                        result.phases[index] = result.phases[index] - 1
                    
                pass
            
            # convert magnitude to flux
            if self.mon.checkState() == Qt.Checked :
                pass
            
            Plot.instance().setImport(result.phases, result.values)
            Plot.instance().redraw()
            
        except:
            QMessageBox.critical(self, "Import error", "Error importing data!")
            
       
        self.close()
        
class ExportPlotDialog(QDialog):
    
    def __init__(self):
        super(ExportPlotDialog, self).__init__()
        self.setWindowTitle('Export plot')
        #self.setWindowIcon(QIcon('assets/export.png'))
        self.resize(400, 200)
        
        
class ExportDatDialog(QFileDialog):
    
    def __init__(self, phases, values, import_phases, import_values):
        super(ExportDatDialog, self).__init__()
        self.setWindowTitle('Export DAT')
        #self.setWindowIcon(QIcon('assets/export.png'))
        self.resize(500, 400)
        self.setFileMode(QFileDialog.AnyFile)
        fname = self.getSaveFileName(directory='result.dat', filter='DAT (*.dat);;')
        
        try:
            
            with open(fname, 'wb') as csvfile:
                csv_writter = csv.writer(csvfile, delimiter="\t")
                for index, phase in enumerate(phases):
                    row = []
                    row.append(str(phase))
                    row.append(str(values[index]))
                    try :
                        import_index = import_phases.index(phase)
                        row.append(str(import_values[import_index]))
                        row.append(str(abs(import_values[import_index] - values[index])))
                            
                    except Exception:
                        pass
                    
                    csv_writter.writerow(row)
                    
        except Exception:
            QMessageBox.warning(self, "Error", "Error exporting!")
            return
    

class CustomDoubleSpinBox(QDoubleSpinBox):
    
    def __init__(self,parent=None,value=0):
        super(CustomDoubleSpinBox, self).__init__(parent)
        
    def textFromValue(self, value):
        result = str(QDoubleSpinBox.textFromValue(self, value))
        if result.find(".") > 0 :
            result = result.rstrip("0")
            result = result.rstrip(".")
        return result
        
class ResultTable(QWidget):

    __instance = None
    
    def __init__(self):
        super(QWidget, self).__init__()

        if ResultTable.__instance is None :
            ResultTable.__instance = self

        self.phases = []
        self.values = []        
        
        self.vbox = QVBoxLayout()
        
        header = ['Phase', 'Synthetic', 'Observation', 'Delta']
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        
        self.vbox.addWidget(self.table)
        
        bhbox = QHBoxLayout()
        bhbox.setAlignment(Qt.AlignRight)
        bexport = QPushButton('Export...')
        bexport.clicked.connect(self._onExport)
        bhbox.addWidget(bexport)
        
        self.vbox.addLayout(bhbox)    

        self.setLayout(self.vbox)
        
    def setData(self, phases, values, import_phases, import_values):
        self.phases = phases
        self.values = values
        self.import_phases = import_phases
        self.import_values = import_values
        self.table.setRowCount(len(phases))
        
        for (index, phase) in enumerate(phases):
            self.table.setItem(index, 0, QTableWidgetItem(str(phase)))
            self.table.setItem(index, 1, QTableWidgetItem(str(values[index])))
            
            try :
                import_index = import_phases.index(phase)
                self.table.setItem(index, 2, QTableWidgetItem(str(import_values[import_index])))
                self.table.setItem(index, 3, QTableWidgetItem(str(abs(import_values[import_index] - values[index]))))
                    
            except Exception:
                pass
        
    def _onExport(self):
        self.export = ExportDatDialog(self.phases, self.values, self.import_phases, self.import_values)
        pass
    
    @staticmethod
    def instance():
        return ResultTable.__instance