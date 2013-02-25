# -*- coding: utf-8 -*-

import sys
import csv
from PyQt4.QtGui import QLineEdit, QColor, QMenu, QHBoxLayout, QVBoxLayout, QGridLayout, QCheckBox, QAbstractItemView, QDoubleSpinBox, QFileDialog, QMessageBox, QGroupBox, QLabel, QDialog, QWidget, QTableWidget, QTableWidgetItem, QTabWidget, QPushButton, QPalette, QSizePolicy
from PyQt4.QtCore import Qt, QString, QLocale
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
from ..Task import TaskImporter
from copy import copy

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
        
        self.residual_plot = ResidualPlot()
        self.residual_plot.setFixedHeight(150)
        vbox.addWidget(self.residual_plot)
        
        self.chihbox = QHBoxLayout()
        self.chihbox.setAlignment(Qt.AlignHCenter)
        self.chi2Label = QLabel('chi^2')
        self.chi2Label.setFixedWidth(30)
        self.chi2Label.hide();
        self.chi2Value = QLineEdit()
        self.chi2Value.setAlignment(Qt.AlignRight)
        self.chi2Value.setFixedWidth(120)
        self.chi2Value.hide()
        self.chihbox.addWidget(self.chi2Label)
        self.chihbox.addWidget(self.chi2Value)
        vbox.addLayout(self.chihbox)
                
        #self.toolbar = QHBoxLayout()
        #self.toolbar.setAlignment(Qt.AlignRight)

        #self.toolbar_import = QPushButton('Import observation...')
        #self.toolbar_import.clicked.connect(self.onImport)
        #self.toolbar.addWidget(self.toolbar_import)

        #self.toolbar_exportplot = QPushButton('Export')
        #self.toolbar_exportplot.clicked.connect(self.onExportPlot)
        #self.toolbar.addWidget(self.toolbar_exportplot)
        
        #vbox.addLayout(self.toolbar)
        self.setLayout(vbox)
        
    def onExportPlot(self):
        # show export dialog
        dlg = ExportPlotDialog()
        dlg.exec_()
        
    def onImport(self):
        dlg = ImportDialog()
        dlg.exec_()
        
class Plot(FigureCanvas):

    __instance = None
    
    import_phases = []
    import_values = []
    
    result_phases = []
    result_values = []
    
    result_import_phases = []
    result_import_values = []
    
    last_xlim = []
    
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
        self.result_import_phases = []
        self.result_import_values = []
        
        
        for import_phase in self.import_phases :
            if abs(import_phase) in self.result_phases :
                self.result_import_phases.append(import_phase)
                self.result_import_values.append(self.result_values[self.result_phases.index(abs(import_phase))])
                
    def setImport(self, phases, values):
        self.import_phases = phases
        self.import_values = values
        
        
    def redraw(self):
        if not self.import_phases :
            ResultTable.instance().setData(self.result_phases, self.result_values, [], [])
            
        self.clear()
        
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.grid(True)
        self.axes.set_xlabel('Phase')
        self.axes.set_ylabel('Flux')
        
        result_phases = copy(self.result_phases)
        result_values = copy(self.result_values)
                        
        for (index, phase) in enumerate(self.result_phases):
            if phase > 0.5 :
                del_index = result_phases.index(phase)
                del result_phases[del_index]
                del result_values[del_index]
                
                result_phases.insert(0, phase - 1)
                result_values.insert(0, self.result_values[index])
            else:
                result_phases.insert(0, -phase)
                result_values.insert(0, self.result_values[index])
            
        import_phases = copy(self.import_phases)
        import_values = copy(self.import_values)
        
        if not result_phases and not import_phases :
            return
        yrmin = 1
        yrmax = 0
        xrmax = 0
        yimin = 1
        yimax = 0
        ximax = 0
        
        if result_values :
            yrmin = min(result_values)
            yrmax = max(result_values)
            xrmax = max(abs(min(result_phases)), abs(max(result_phases)))
    
        if import_values :
            yimin = min(import_values)
            yimax = max(import_values)
            ximax = max(abs(min(import_phases)), abs(max(import_phases)))
            
        ymax = max(yrmax, yimax)
        ymin = min(yrmin, yimin)
        xmax = max(xrmax, ximax)
        ypad = ((ymax - ymin) / 100) * 10
        xpad = (xmax / 100) * 10
        
        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim([ymin - ypad, ymax + ypad])

        self.last_xlim = [-(xmax + xpad), xmax + xpad]                        
        self.axes.set_autoscalex_on(False)
        self.axes.set_xlim(self.last_xlim)
        
        
        if len(self.result_phases):
            self.axes.plot(result_phases, result_values, color='b', label="Prediction")
        
        if len(self.import_phases):
            self.axes.scatter(import_phases, import_values, s=1, color='r', label='Observation')
                
        self.draw()
        
class ResidualPlot(FigureCanvas):
    
    __instance = None
            
    def __init__(self):
        if ResidualPlot.__instance is None :
            ResidualPlot.__instance = self
        else:
            raise Exception("ResidualPlot is singleton!")

        self.chi2s = []
        bgColor = str(QPalette().color(QPalette.Active, QPalette.Window).name())
        rcParams.update({'font.size': 10})        
                    
        self.figure = Figure(facecolor=bgColor, edgecolor=bgColor)
        self.figure.hold(False)
        super(ResidualPlot, self).__init__(self.figure)
        
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.hide()        
        
    @staticmethod
    def instance():
        return ResidualPlot.__instance
        
    def clear(self):
        self.figure.clear()
        self.draw()
        
            
    def redraw(self):
        self.clear()
        
        if len(Plot.instance().result_import_phases) == 0 :
            self.parent().chi2Label.hide()
            self.parent().chi2Value.hide()
            self.hide()
            return

        self.show()
        self.parent().chi2Label.show()
        self.parent().chi2Value.show()
        
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.grid(False)
        self.figure.set_alpha(0)
        self.axes.set_xlabel('Phase')
        self.axes.set_ylabel('Residual')
        
                        
                        
        dphases = []        
        dfluxes = []
                      
        for index, phase in enumerate(Plot.instance().result_import_phases):
            dphases.append(phase)
            dfluxes.append(Plot.instance().import_values[Plot.instance().import_phases.index(phase)] - Plot.instance().result_import_values[index])
            
        ymax = max(abs(min(dfluxes)), abs(max(dfluxes)))
        ypad = (ymax / 100) * 10
        
        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim([-(ymax + ypad), ymax + ypad])
        
        self.axes.set_autoscalex_on(False)
        self.axes.set_xlim(Plot.instance().last_xlim)

        chi2 = 0        
        for dflux in dfluxes :
            chi2 = chi2 + dflux**2
            
        self.chi2s.append(chi2) 
        
        color = QColor(0,0,0)
        minChi2 = min(self.chi2s)
        if len(self.chi2s) == 1 :
            color = QColor(0,0,0)
        elif chi2 <= minChi2 :
            color = QColor(0,139,0)
        else:
            color = QColor(255,0,0)
            
        ResultTable.instance().setData(Plot.instance().result_phases, Plot.instance().result_values, Plot.instance().import_phases, Plot.instance().import_values)
        
        self.axes.axhline(y=0, ls='--', linewidth=0.5, color='black')
        self.axes.scatter(dphases, dfluxes, s=0.5, color='r')
        #self.axes.text(0.98, 0.95, 'chi^2= ' + str(chi2), color=color, horizontalalignment='right', verticalalignment='top', transform = self.axes.transAxes)
        palette = self.parent().chi2Value.palette()
        palette.setColor(QPalette.Active, QPalette.Text, color)
        self.parent().chi2Value.setPalette(palette)
        self.parent().chi2Value.setText(str(chi2))
        
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
        self.mon.stateChanged.connect(self._onMagCheck)
        grid.addWidget(self.mon, 1, 0, 1, 0)

        self.mmaxl = QLabel('Mag')
        self.mmax = CustomDoubleSpinBox()
        self.mmax.setSingleStep(0.01)
        self.mmax.setDecimals(10)
        self.mmax.setAccelerated(True)
        self.mmax.setDisabled(True)
        self.mmax.setMinimum(0)
        self.mmax.setFixedWidth(120)
        grid.addWidget(self.mmaxl, 2, 0)
        grid.addWidget(self.mmax, 2, 1)
                
        
        self.son = QCheckBox('Convert HJD to phases')
        self.son.stateChanged.connect(self._onJDTCheck)
        grid.addWidget(self.son, 4, 0, 1, 0)
        
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
        grid.addWidget(self.tzerol, 5, 0)
        grid.addWidget(self.tzero, 5, 1)
        
        self.periodl = QLabel('P')
        self.periodl.setFixedWidth(60)
        self.period = CustomDoubleSpinBox()
        self.period.setFixedWidth(120)
        self.period.setDisabled(True)
        self.period.setRange(0, sys.float_info.max)
        self.period.setDecimals(10)
        grid.addWidget(self.periodl, 6, 0)
        grid.addWidget(self.period, 6, 1)
        
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
    
    def _onMagCheck(self, state):
        if state == Qt.Checked :
            self.mmax.setDisabled(False)
        else:
            self.mmax.setDisabled(True)
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
            
       
        self.close()
        
class ExportPlotDialog(QDialog):
    
    def __init__(self):
        super(ExportPlotDialog, self).__init__()
        self.setWindowTitle('Export plot')
        #self.setWindowIcon(QIcon('assets/export.png'))
        self.resize(400, 200)
        
        
class ExportDatDialog(QFileDialog):
    
    def __init__(self, phases, values, import_phases, import_values, separator):
        super(ExportDatDialog, self).__init__()
        self.setWindowTitle('Export DAT')
        #self.setWindowIcon(QIcon('assets/export.png'))
        self.resize(500, 400)
        self.setFileMode(QFileDialog.AnyFile)
        fname = self.getSaveFileName(directory='result.dat', filter='DAT (*.dat);;')
                
        try:
            
            with open(fname, 'wb') as csvfile:
                csv_writter = csv.writer(csvfile, delimiter=separator)
                for index, phase in enumerate(phases):
                    row = []
                    row.append('%.12f' % phase)
                    row.append('%.12f' % values[index])
                    
                    if phase in import_phases :
                        import_index = import_phases.index(phase)
                        row.append('%.12f' % import_values[import_index])
                        row.append('%.12f' % (import_values[import_index] - values[index]))
                            
                    csv_writter.writerow(row)
                    
        except:
            QMessageBox.warning(self, "Error", "Error exporting!\nError: " + str(sys.exc_info()[1]))
            raise
    

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
        bexport_menu = QMenu()
        bexport_menu.addAction('\\t separated').triggered.connect(lambda : self._onExport('\t'))
        bexport_menu.addAction(', separated').triggered.connect(lambda : self._onExport(','))
        bexport_menu.addAction('; separated').triggered.connect(lambda : self._onExport(';'))
        bexport.setMenu(bexport_menu)        
        bhbox.addWidget(bexport)
        
        self.vbox.addLayout(bhbox)    

        self.setLayout(self.vbox)
        
    def setData(self, phases, values, import_phases, import_values):
        
        self.phases = []
        self.values = []
        
        for (index, phase) in enumerate(phases):
            if phase == 0 :
                continue
            
            self.phases.insert(0, -phase)
            self.values.insert(0, values[index])
                   
        for (index, phase) in enumerate(phases):
            self.phases.append(phase)
            self.values.append(values[index])
            
        self.import_phases = import_phases
        self.import_values = import_values
        
        self.table.setRowCount(len(self.phases))

        for (index, phase) in enumerate(self.phases):
            phase_item = QTableWidgetItem('%.12f' % phase)
            phase_item.setTextAlignment(Qt.AlignRight)

            value_item = QTableWidgetItem('%.12f' % self.values[index])
            value_item.setTextAlignment(Qt.AlignRight)
            self.table.setItem(index, 0, phase_item)
            self.table.setItem(index, 1, value_item)
            
            if phase in import_phases :
                import_index = import_phases.index(phase)
                
                ivalue_item = QTableWidgetItem('%.12f' % import_values[import_index])
                ivalue_item.setTextAlignment(Qt.AlignRight)
                
                idflux_item = QTableWidgetItem('%.12f' % (import_values[import_index] - self.values[index]))
                idflux_item.setTextAlignment(Qt.AlignRight)
                
                self.table.setItem(index, 2, ivalue_item)
                self.table.setItem(index, 3, idflux_item)
        
    def _onExport(self, separator):
        self.export = ExportDatDialog(self.phases, self.values, self.import_phases, self.import_values, separator)
        pass
    
    @staticmethod
    def instance():
        return ResultTable.__instance