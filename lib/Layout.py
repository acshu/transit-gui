# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from ast import literal_eval
from copy import copy
from genericpath import exists
from math import atan, degrees, sin, sqrt, log10
import operator
import os
import sys
import csv
from PyQt4.QtCore import Qt, pyqtSignal, QString, QAbstractTableModel, QVariant, QEvent

from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QProgressBar, QGridLayout, QLabel, QCheckBox, QFileDialog, QMessageBox, QTabWidget, QLineEdit, QPalette, QSizePolicy, QColor, QTableWidget, QAbstractItemView, QMenu, QTableWidgetItem, QTableView, QAction
import math
import gc
from matplotlib import rcParams
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from lib.Structures import Global, TaskRange
from lib.Utils import Constants, TaskImporter, flip_phase_list, uc_variable_name
from lib.FormParams import *


class Layout(QWidget):
    
    def __init__(self):
        super(Layout, self).__init__()
        self.setLayout(QHBoxLayout())
                        
        self.form = InputForm()
        self.result = ResultView()
        self.setObjectName('Layout')
        
        self.layout().addWidget(self.form)
        self.layout().addWidget(self.result)


class InputForm(QWidget):

    __instance = None

    @staticmethod
    def instance():
        return InputForm.__instance

    def __init__(self):
        if not InputForm.__instance:
            InputForm.__instance = self

        super(InputForm, self).__init__()

        Global.event.task_started.connect(self._on_task_started)
        Global.event.task_completed.connect(self._on_task_completed)
        Global.event.task_progressed.connect(self._on_task_progressed)
        Global.event.task_range_progressed.connect(self._on_task_range_progressed)
        Global.event.interface_load_task_params.connect(self._on_interface_load_task_params)

        self.vl = QVBoxLayout()
        self.vl.setContentsMargins(0,0,0,0)

        self.setLayout(self.vl)
        self.setFixedWidth(290)

        self.tab = QTabWidget()
        self.vl.addWidget(self.tab)

        self.input_parameters = InputParameters()
        self.input_parameters.ranges_state_changed.connect(self._on_ranges_state_changed)
        self.tab.addTab(self.input_parameters, 'Parameters')

        self.import_parameters = ImportParameters()
        self.tab.addTab(self.import_parameters, 'Observation')

        control_buttons = QWidget()
        control_buttons.setLayout(QVBoxLayout())
        control_buttons.layout().setContentsMargins(0, 0, 0, 0)
        control_buttons.layout().setAlignment(Qt.AlignBottom)

        self._progress = QProgressBar()
        self._progress.setValue(0)
        self._progress.setTextVisible(True)
        self._progress.setAlignment(Qt.AlignCenter)
        self._progress.hide()
        control_buttons.layout().addWidget(self._progress)

        self._range_progress = QProgressBar()
        self._range_progress.setValue(0)
        self._range_progress.setTextVisible(True)
        self._range_progress.setAlignment(Qt.AlignCenter)
        self._range_progress.hide()
        control_buttons.layout().addWidget(self._range_progress)

        self._calculate = QPushButton('Calculate')
        self._calculate.clicked.connect(self._on_calculate)
        control_buttons.layout().addWidget(self._calculate)

        self._cancel = QPushButton('Cancel')
        self._cancel.hide()
        self._cancel.clicked.connect(self._on_cancel)
        control_buttons.layout().addWidget(self._cancel)

        self.vl.addWidget(control_buttons)

        if exists("./config/last-session.ini") :
            self.load_params("./config/last-session.ini")

    def _on_ranges_state_changed(self, parameters):
        Global.task_range().reset()

        if len(parameters):
            keys = parameters.keys()
            for key in parameters:
                Global.task_range().set_range(key, copy(parameters[key].range.values))

            self._calculate.setText('Calculate ' + str(Global.task_range()._total_count) + ' variations')
        else:
            self._calculate.setText('Calculate')

    def _on_calculate(self):
        self.import_parameters.import_observation()

        combination = Global.task_range().get_next_combination()

        Global.task().input.semi_major_axis = self.input_parameters.semi_major_axis.getValue()
        Global.task().input.star_radius = self.input_parameters.star_radius.getValue()
        Global.task().input.planet_radius = self.input_parameters.planet_radius.getValue()
        Global.task().input.star_temperature = self.input_parameters.star_temperature.getValue()
        Global.task().input.planet_temperature = self.input_parameters.planet_temperature.getValue()
        Global.task().input.darkening_law = self.input_parameters.darkening_law.value.itemData(self.input_parameters.darkening_law.value.currentIndex()).toString()
        Global.task().input.darkening_1 = self.input_parameters.darkening_coefficient_1.getValue()
        Global.task().input.darkening_2 = self.input_parameters.darkening_coefficient_2.getValue()
        Global.task().input.inclination = self.input_parameters.inclination.getValue()
        Global.task().input.phase_start = 0
        Global.task().input.phase_end = self.input_parameters.phase_end.getValue()
        Global.task().input.phase_step = self.input_parameters.phase_step.getValue()
        Global.task().input.precision = 10**self.input_parameters.integration_precision.getValue()

        if combination:
            for param in combination:
                setattr(Global.task().input, param[0], param[1])

        Global.task().start()

    def _on_task_range_progressed(self, progress):
        self._range_progress.setFormat( str(Global.task_range().completed_count()) + ' of ' + str(Global.task_range().total_count()))
        self._range_progress.setValue(math.ceil(((float(Global.task_range().completed_count()))/Global.task_range().total_count())*100))
        self._on_calculate()

    def _on_task_started(self, task):
        self._calculate.hide()
        self._progress.show()
        self._progress.setValue(0)
        self._cancel.show()
        self.tab.setDisabled(True)

        if Global.task_range().total_count():
            self._range_progress.show()
            if Global.task_range().completed_count() == 0:
                self._range_progress.setFormat('0 of ' + str(Global.task_range().total_count()))
                self._range_progress.setValue(0)

    def _on_task_progressed(self, task, progress):
        self._progress.setValue(progress)

    def _on_task_completed(self, task):
        if Global.task_range().total_count() and Global.task_range().completed_count():
            return

        self._calculate.show()
        self._progress.hide()
        self._progress.setValue(0)
        self._cancel.hide()
        self.tab.setDisabled(False)
        self._range_progress.hide()
        self._range_progress.setValue(0)

    def _on_cancel(self):
        Global.task().stop()

        self._calculate.show()
        self._progress.hide()
        self._progress.setValue(0)
        self._range_progress.hide()
        self._range_progress.setValue(0)
        self._cancel.hide()
        self.tab.setDisabled(False)

    def _on_interface_load_task_params(self, task):
        self.input_parameters.semi_major_axis.value.setValue(task.input.semi_major_axis)
        self.input_parameters.star_radius.value.setValue(task.input.star_radius)
        self.input_parameters.planet_radius.value.setValue(task.input.planet_radius)
        self.input_parameters.star_temperature.value.setValue(task.input.star_temperature)
        self.input_parameters.planet_temperature.value.setValue(task.input.planet_temperature)
        self.input_parameters.inclination.value.setValue(task.input.inclination)

        darkening_law_index = 0
        for item in DarkeningLaw.items:
            if item[1] == task.input.darkening_law:
                break
            darkening_law_index += 1

        self.input_parameters.darkening_law.value.setCurrentIndex(darkening_law_index)
        self.input_parameters.darkening_coefficient_1.value.setValue(task.input.darkening_1)
        self.input_parameters.darkening_coefficient_2.value.setValue(task.input.darkening_2)
        self.input_parameters.phase_end.value.setValue(task.input.phase_end)
        self.input_parameters.phase_step.value.setValue(task.input.phase_step)
        self.input_parameters.integration_precision.value.setValue(log10(task.input.precision))

        for parameter_name in copy(self.input_parameters.range_parameters):
            parameter = getattr(self.input_parameters, parameter_name)
            if parameter.range:
                parameter.range.set_active(False)

        self.repaint()

    def load_params(self, filename):
        config = ConfigParser()
        config.read(filename)

        self._normalize_config(config)

        # Input Parameters
        self._load_config_param(config, 'input', 'semi_major_axis')
        self._load_config_param(config, 'input', 'star_radius')
        self._load_config_param(config, 'input', 'planet_radius')
        self._load_config_param(config, 'input', 'star_temperature')
        self._load_config_param(config, 'input', 'planet_temperature')
        self._load_config_param(config, 'input', 'inclination')
        self._load_config_param(config, 'input', 'darkening_law')
        self._load_config_param(config, 'input', 'darkening_coefficient_1')
        self._load_config_param(config, 'input', 'darkening_coefficient_2')
        self._load_config_param(config, 'input', 'phase_end')
        self._load_config_param(config, 'input', 'phase_step')
        self._load_config_param(config, 'input', 'integration_precision')

        # Import Parameters
        if config.has_option('import', 'filename') and config.get('import', 'filename'):
            if '/data/' in config.get('import', 'filename') and config.get('import', 'filename').index('/data/') == 0:
                self.import_parameters.filename = os.getcwd().replace('\\', '/') + config.get('import', 'filename')
            else:
                self.import_parameters.filename = config.get('import', 'filename')

        self.import_parameters.update_file_label()

        if config.has_option('import', 'jd2phase') and config.getboolean('import', 'jd2phase') == True :
            self.import_parameters.hjd_to_phases.setCheckState(Qt.Checked)

        if config.has_option('import', 'jd2phase_tzero') :
            self.import_parameters.time_zero.setValue(config.getfloat('import', 'jd2phase_tzero'))

        if config.has_option('import', 'jd2phase_period') :
            self.import_parameters.period.setValue(config.getfloat('import', 'jd2phase_period'))

        if config.has_option('import', 'mag2flux') and config.getboolean('import', 'mag2flux') == True :
            self.import_parameters.magnitude_to_flux.setCheckState(Qt.Checked)

        if config.has_option('import', 'mag2flux_mag') :
            self.import_parameters.magnitude_max.setValue(config.getfloat('import', 'mag2flux_mag'))

        # Fixes painting bug with range buttons when loading new file
        # the active ranges stayed active even if they are inactive
        self.repaint()

    def _normalize_config(self, config):
        if config.has_option('input', 'darkening_1'):
            config.set('input', 'darkening_coefficient_1', config.get('input', 'darkening_1'))
            config.remove_option('input', 'darkening_1')

        if config.has_option('input', 'darkening_2'):
            config.set('input', 'darkening_coefficient_2', config.get('input', 'darkening_2'))
            config.remove_option('input', 'darkening_2')

        if config.has_option('input', 'precision'):
            config.set('input', 'integration_precision', config.get('input', 'precision'))
            config.remove_option('input', 'precision')

    def _load_config_param(self, config, section, name):
        param = getattr(self.input_parameters, name)

        if config.has_option(section, name):
            if type(param.value) is QComboBox:
                param.value.setCurrentIndex(config.getint(section, name))
            else:
                param.value.setValue(literal_eval(config.get(section, name)))

        if param.range:
            _from = _to = _step = _values = None
            _active = False

            if config.has_option(section, name + '_range_from'):
                _from = literal_eval(config.get(section, name + '_range_from'))

            if config.has_option(section, name + '_range_to'):
                _to = literal_eval(config.get(section, name + '_range_to'))

            if config.has_option(section, name + '_range_step'):
                _step = literal_eval(config.get(section, name + '_range_step'))

            if config.has_option(section, name + '_range_values'):
                _values = literal_eval(config.get(section, name + '_range_values'))

            if config.has_option(section, name + '_range_active'):
                _active = config.getboolean(section, name + '_range_active')

            if _values:
                param.range.set_range(_values)
            elif _from and _to and _step:
                param.range.set_range(_from, _to, _step)

            param.range.set_active(_active)

    def _save_config_param(self, config, section, name):
        param = getattr(self.input_parameters, name)

        if type(param.value) is QComboBox:
            config.set(section, name, param.value.currentIndex())
        else:
            config.set(section, name, param.getValue())

        if param.range:
            if param.range.range_from and param.range.range_to and param.range.range_step:
                config.set(section, name + '_range_from', param.range.range_from)
                config.set(section, name + '_range_to', param.range.range_to)
                config.set(section, name + '_range_step', param.range.range_step)
            elif param.range.values:
                config.set(section, name + '_range_values', param.range.values)

            if param.range.is_active():
                config.set(section, name + '_range_active', param.range.is_active())

    def save_params(self, filename):
        config = ConfigParser()
        config.add_section('input')

        # Input Parameters
        self._save_config_param(config, 'input', 'semi_major_axis')
        self._save_config_param(config, 'input', 'star_radius')
        self._save_config_param(config, 'input', 'planet_radius')
        self._save_config_param(config, 'input', 'star_temperature')
        self._save_config_param(config, 'input', 'planet_temperature')
        self._save_config_param(config, 'input', 'inclination')
        self._save_config_param(config, 'input', 'darkening_law')
        self._save_config_param(config, 'input', 'darkening_coefficient_1')
        self._save_config_param(config, 'input', 'darkening_coefficient_2')
        self._save_config_param(config, 'input', 'phase_end')
        self._save_config_param(config, 'input', 'phase_step')
        self._save_config_param(config, 'input', 'integration_precision')

        config.add_section('import')

        if os.getcwd().replace('\\', '/') in str(self.import_parameters.filename) and str(self.import_parameters.filename).index(os.getcwd().replace('\\', '/')) == 0 :
            save_file_path = str(self.import_parameters.filename).replace(os.getcwd().replace('\\', '/'), '')
        else:
            save_file_path = str(self.import_parameters.filename)

        config.set('import', 'filename', save_file_path)
        config.set('import', 'jd2phase', self.import_parameters.hjd_to_phases.checkState() == Qt.Checked)
        config.set('import', 'jd2phase_tzero', self.import_parameters.time_zero.value())
        config.set('import', 'jd2phase_period', self.import_parameters.period.value())
        config.set('import', 'mag2flux', self.import_parameters.magnitude_to_flux.checkState() == Qt.Checked)
        config.set('import', 'mag2flux_mag', self.import_parameters.magnitude_max.value())

        with open(filename, 'wb') as configfile:
            config.write(configfile)
        pass


class InputParameters(QWidget):

    ranges_state_changed = pyqtSignal(dict)

    def __init__(self):
        QWidget.__init__(self)

        self.range_parameters = dict()

        self.grid = QGridLayout()
        self.grid.setAlignment(Qt.AlignTop)
        self.grid.setColumnStretch(2, 2)

        self.setLayout(self.grid)

        # Semi-major axis
        self.semi_major_axis = self.add_triplet(SemiMajorAxis(), 1)
        self.semi_major_axis.range.clicked.connect(lambda: self._on_range_clicked('semi_major_axis'))
        self.semi_major_axis.range.state_changed.connect(self.semi_major_axis.value.setDisabled)
        self.semi_major_axis.range.state_changed.connect(lambda: self._on_range_changed('semi_major_axis'))

        # Star radius
        self.star_radius = self.add_triplet(StarRadiusAU(), 2)
        self.star_radius_rs = self.add_triplet(StarRadiusRS(), 3)
        self.star_radius.range.clicked.connect(lambda: self._on_range_clicked('star_radius'))
        self.star_radius.range.state_changed.connect(self.star_radius.value.setDisabled)
        self.star_radius.range.state_changed.connect(self.star_radius_rs.value.setDisabled)
        self.star_radius.range.state_changed.connect(lambda: self._on_range_changed('star_radius'))

        self.star_radius.value.valueChanged.connect(self._on_star_radius_change)
        self.star_radius_rs.value.valueChanged.connect(self._on_star_radius_rs_change)

        # Planet radius
        self.planet_radius = self.add_triplet(PlanetRadiusAU(), 4)
        self.planet_radius_rj = self.add_triplet(PlanetRadiusRJ(), 5)
        self.planet_radius.range.clicked.connect(lambda: self._on_range_clicked('planet_radius'))
        self.planet_radius.range.state_changed.connect(self.planet_radius.value.setDisabled)
        self.planet_radius.range.state_changed.connect(self.planet_radius_rj.value.setDisabled)
        self.planet_radius.range.state_changed.connect(lambda: self._on_range_changed('planet_radius'))

        self.planet_radius.value.valueChanged.connect(self._on_planet_radius_change)
        self.planet_radius_rj.value.valueChanged.connect(self._on_planet_radius_rj_change)

        # Star temperature
        self.star_temperature = self.add_triplet(StarTemperature(), 6)
        self.star_temperature.range.clicked.connect(lambda: self._on_range_clicked('star_temperature'))
        self.star_temperature.range.state_changed.connect(self.star_temperature.value.setDisabled)
        self.star_temperature.range.state_changed.connect(lambda: self._on_range_changed('star_temperature'))

        # Planet temperature
        self.planet_temperature = self.add_triplet(PlanetTemperature(), 7)
        self.planet_temperature.range.clicked.connect(lambda: self._on_range_clicked('planet_temperature'))
        self.planet_temperature.range.state_changed.connect(self.planet_temperature.value.setDisabled)
        self.planet_temperature.range.state_changed.connect(lambda: self._on_range_changed('planet_temperature'))

        # Inclination
        self.inclination = self.add_triplet(Inclination(), 8)
        self.inclination.range.clicked.connect(lambda: self._on_range_clicked('inclination'))
        self.inclination.range.state_changed.connect(self.inclination.value.setDisabled)
        self.inclination.range.state_changed.connect(lambda: self._on_range_changed('inclination'))

        # Darkening law
        self.darkening_law = self.add_triplet(DarkeningLaw(), 9)
        self.darkening_law.range.clicked.connect(lambda: self._on_range_clicked('darkening_law'))
        self.darkening_law.range.state_changed.connect(self.darkening_law.value.setDisabled)
        self.darkening_law.range.state_changed.connect(lambda: self._on_range_changed('darkening_law'))

        # Darkening coefficients
        self.darkening_coefficient_1 = self.add_triplet(DarkeningCoefficient('Dark. coefficient 1:', ''), 10)
        self.darkening_coefficient_1.range.clicked.connect(lambda: self._on_range_clicked('darkening_coefficient_1'))
        self.darkening_coefficient_1.range.state_changed.connect(self.darkening_coefficient_1.value.setDisabled)
        self.darkening_coefficient_1.range.state_changed.connect(lambda: self._on_range_changed('darkening_coefficient_1'))

        self.darkening_coefficient_2 = self.add_triplet(DarkeningCoefficient('Dark. coefficient 2:', ''), 11)
        self.darkening_coefficient_2.range.clicked.connect(lambda: self._on_range_clicked('darkening_coefficient_2'))
        self.darkening_coefficient_2.range.state_changed.connect(self.darkening_coefficient_2.value.setDisabled)
        self.darkening_coefficient_2.range.state_changed.connect(lambda: self._on_range_changed('darkening_coefficient_2'))

        # Phase end
        self.phase_end = self.add_triplet(PhaseEnd(), 12)

        # Phase step
        self.phase_step = self.add_triplet(PhaseStep(), 13)

        # integration precision
        self.integration_precision = self.add_triplet(IntegrationPrecision(), 14)

    def _on_star_radius_change(self, value):
        self.star_radius_rs.value.blockSignals(True)
        self.star_radius_rs.value.setValue(Constants.au_to_rs(value))
        self.star_radius_rs.value.blockSignals(False)

    def _on_star_radius_rs_change(self, value):
        self.star_radius.value.blockSignals(True)
        self.star_radius.value.setValue(Constants.rs_to_au(value))
        self.star_radius.value.blockSignals(False)

    def _on_planet_radius_change(self, value):
        self.planet_radius_rj.value.blockSignals(True)
        self.planet_radius_rj.value.setValue(Constants.au_to_rj(value))
        self.planet_radius_rj.value.blockSignals(False)

    def _on_planet_radius_rj_change(self, value):
        self.planet_radius.value.blockSignals(True)
        self.planet_radius.value.setValue(Constants.rj_to_au(value))
        self.planet_radius.value.blockSignals(False)

    def _on_range_clicked(self, name):
        if not getattr(self, name).range.is_active():
            if getattr(self, name) == self.darkening_law:
                dialog = getattr(sys.modules[__name__], uc_variable_name(name) + 'RangeDialog')(getattr(self, name).range.values)
            else:
                dialog = getattr(sys.modules[__name__], uc_variable_name(name) + 'RangeDialog')(getattr(self, name).range.range_from, getattr(self, name).range.range_to, getattr(self, name).range.range_step)
            dialog.accepted.connect(lambda: self._on_range_accepted(name))
            dialog.rejected.connect(lambda: self._on_range_rejected(name))
            dialog.display()
        else:
            self._on_range_rejected(name)
            pass

    def _on_range_accepted(self, name):
        if getattr(self, name) == self.darkening_law:
            getattr(self, name).range.set_range(self.sender().values())
        else:
            getattr(self, name).range.set_range(getattr(self.sender(), name + '_from').getValue(),
                                                getattr(self.sender(), name + '_to').getValue(),
                                                getattr(self.sender(), name + '_step').getValue())
        getattr(self, name).range.set_active(True)

    def _on_range_rejected(self, name):
        getattr(self, name).range.set_active(False)

        if name == 'planet_radius':
            self.planet_radius_rj.value.setDisabled(False)

    def _on_range_changed(self, name):
        if getattr(self, name).range.is_active():
            self.range_parameters[name] = getattr(self, name)
        elif self.range_parameters.has_key(name):
            del self.range_parameters[name]

        self.ranges_state_changed.emit(self.range_parameters)

    def add_triplet(self, triplet, position):
        self.grid.addWidget(triplet.label, position, 0)
        self.grid.addWidget(triplet.range, position, 1)
        self.grid.addWidget(triplet.value, position, 2)
        self.grid.addWidget(triplet.unit, position, 3)
        return triplet


class ImportParameters(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.filename = ''
        self.import_phases = []
        self.import_values = []

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)

        self.setLayout(grid)

        self.filename_label = QLabel('No file selected')
        self.file_browse = QPushButton('Browse...')
        self.file_browse.setFixedWidth(85)
        self.file_browse.clicked.connect(self._on_file_browse)
        self.file_clear = QPushButton('Clear')
        self.file_clear.setFixedWidth(85)
        self.file_clear.clicked.connect(self._on_file_clear)
        self.file_clear.setHidden(True)
        grid.addWidget(self.filename_label, 1, 0, 1, 0)
        grid.addWidget(self.file_browse, 1, 3)
        grid.addWidget(self.file_clear, 1, 3)

        self.hjd_to_phases = QCheckBox('Convert HJD to phases')
        self.hjd_to_phases.stateChanged.connect(self._on_hjd_state_changed)
        grid.addWidget(self.hjd_to_phases, 2, 0, 1, 0)

        self.time_zero_label = QLabel('T<sub>0</sub>')
        self.time_zero_label.setFixedWidth(20)
        self.time_zero = CustomDoubleSpinBox()
        self.time_zero.setSingleStep(0.01)
        self.time_zero.setDecimals(10)
        self.time_zero.setAccelerated(True)
        self.time_zero.setDisabled(True)
        self.time_zero.setMinimum(0)
        self.time_zero.setFixedWidth(200)
        self.time_zero.setRange(0, sys.float_info.max)
        grid.addWidget(self.time_zero_label, 3, 0)
        grid.addWidget(self.time_zero, 3, 1)

        self.period_label = QLabel('P')
        self.period_label.setFixedWidth(20)
        self.period = CustomDoubleSpinBox()
        self.period.setFixedWidth(200)
        self.period.setDisabled(True)
        self.period.setRange(0, sys.float_info.max)
        self.period.setDecimals(10)
        grid.addWidget(self.period_label, 4, 0)
        grid.addWidget(self.period, 4, 1)

        self.magnitude_to_flux = QCheckBox('Convert magnitude to flux')
        self.magnitude_to_flux.stateChanged.connect(self._on_magnitude_state_changed)
        grid.addWidget(self.magnitude_to_flux, 5, 0, 1, 0)

        self.magnitude_max_label = QLabel('Mag')
        self.magnitude_max = CustomDoubleSpinBox()
        self.magnitude_max.setSingleStep(0.01)
        self.magnitude_max.setDecimals(10)
        self.magnitude_max.setAccelerated(True)
        self.magnitude_max.setDisabled(True)
        self.magnitude_max.setMinimum(0)
        self.magnitude_max.setFixedWidth(105)
        grid.addWidget(self.magnitude_max_label, 6, 0)
        grid.addWidget(self.magnitude_max, 6, 1)

        self.redraw = QPushButton("Redraw")
        self.redraw.clicked.connect(self._on_redraw)
        grid.addWidget(self.redraw, 6,3)

    def _on_file_browse(self):

        directory = "" if self.filename is None else QString(str("/").join(str(self.filename).split("/")[:-1]))
        types = TaskImporter.get_formats()
        filters = []

        for value in types :
            filters.append(value.upper() + " (*." + value + ")")

        filters.append("All files (*.*)")

        self.filename = QFileDialog.getOpenFileName(self, 'Open file', directory=directory, filter=";;".join(filters))

        self.update_file_label()

    def _on_file_clear(self):
        self.filename = ''
        self.update_file_label()

    def update_file_label(self):
        if self.filename :
            self.filename_label.setText(self.filename.split("/")[-1])
            self.file_clear.setHidden(False)
            self.redraw.setDisabled(False)
        else:
            self.filename_label.setText('No file selected')
            self.file_clear.setHidden(True)
            self.redraw.setDisabled(True)
        pass

    def import_observation(self):
        if not self.filename :
            return

        try:
            phases, values = TaskImporter.load_file(self.filename)

            # convert JD time to phases
            if self.hjd_to_phases.checkState() == Qt.Checked:
                if self.time_zero.value() <= 0 :
                    QMessageBox.warning(self, "Error", 'Invalid parameter "T<sub>0</sub>"!')
                    return

                if self.period.value() <= 0 :
                    QMessageBox.warning(self, "Error", 'Invalid parameter "P"!')
                    return

                for (index, phase) in enumerate(phases):
                    phases[index] = (phase - self.time_zero.value()) / self.period.value() % 1

            # convert magnitude to flux
            if self.magnitude_to_flux.checkState() == Qt.Checked:
                for (index, value) in enumerate(values):
                    values[index] = 10**(-(value - self.magnitude_max.value())/2.5)

            phases = flip_phase_list(phases)

            # TODO Detrending
            #slope = (values[8] - values[-8])/(phases[8] - phases[-8])
            #angle = atan(slope)
            #
            #for index, value in enumerate(values):
            #    hyp = sqrt(abs((phases[-8] - phases[index])**2 - (values[-8] - values[index])**2))
            #    print hyp
            #    values[index] += hyp * sin(angle)

            self.import_phases = phases
            self.import_values = values

            Global.event.data_imported.emit(self.import_phases, self.import_values)

        except:
            QMessageBox.critical(self, "Import error", "Error importing data!\nError: " + str(sys.exc_info()[1]))
            raise

    def _on_redraw(self):
        if not self.filename :
            QMessageBox.warning(self, "Import file", "Please import file first")
            return

        self.import_observation()
        Global.event.interface_redraw_clicked.emit()
        pass

    def _on_hjd_state_changed(self, state):
        if state == Qt.Checked:
            self.time_zero.setDisabled(False)
            self.period.setDisabled(False)
        else:
            self.time_zero.setDisabled(True)
            self.period.setDisabled(True)
        pass

    def _on_magnitude_state_changed(self, state):
        if state == Qt.Checked:
            self.magnitude_max.setDisabled(False)
        else:
            self.magnitude_max.setDisabled(True)
        pass


class ResultView(QTabWidget):

    def __init__(self):
        super(ResultView, self).__init__()

        self.results = ResultsTab()
        self.addTab(self.results, 'Results')

        self.plot = ResultPlot()
        self.addTab(self.plot, 'Plot')

        self.data = ResultTab()
        self.addTab(self.data, 'Data')

        self.setCurrentIndex(1)
        Global.event.task_selected.connect(self._on_task_selected)

    def _on_task_selected(self, task):
        self.setCurrentIndex(1)


class ResultPlot(QWidget):

    def __init__(self):
        super(ResultPlot, self).__init__()
        vl = QVBoxLayout()
        self.plot = Plot()
        vl.setAlignment(Qt.AlignTop)
        vl.addWidget(self.plot)

        self.residual_plot = ResidualPlot()
        self.residual_plot.setFixedHeight(150)
        vl.addWidget(self.residual_plot)

        hl = QHBoxLayout()
        #hl.setAlignment(Qt.AlignHCenter)

        self.chi2_label = QLabel('chi^2')
        self.chi2_label.setFixedWidth(30)
        self.chi2_label.hide();
        self.chi2_value = QLineEdit()
        self.chi2_value.setAlignment(Qt.AlignRight)
        self.chi2_value.setFixedWidth(120)
        self.chi2_value.hide()

        auto_plot =  QCheckBox('Auto plot finished result')
        auto_plot.stateChanged.connect(self._on_auto_plot_state_changed)
        hl.addWidget(auto_plot, Qt.AlignLeft)
        hl.addWidget(self.chi2_label)
        hl.addWidget(self.chi2_value)
        hl.setStretch(1, 0)

        vl.addLayout(hl)
        self.setLayout(vl)

    def _on_auto_plot_state_changed(self, checked_state):
        checked_state = True if checked_state else False
        Global.event.interface_auto_plot_state_changed.emit(checked_state)


class Plot(FigureCanvas):

    __instance = None

    def __init__(self):
        Global.event.task_selected.connect(self._on_task_selected)
        Global.event.task_deleted.connect(self._on_task_deleted)
        Global.event.tasks_list_updated.connect(self._on_tasks_list_updated)

        self.task = None
        self.last_x_limit = []
        self.axes = None

        bg_color = str(QPalette().color(QPalette.Active, QPalette.Window).name())
        rcParams.update({'font.size': 10})

        self.figure = Figure(facecolor=bg_color, edgecolor=bg_color)
        self.figure.hold(False)
        super(Plot, self).__init__(self.figure)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

    def _on_task_selected(self, task):
        self.set_task(task)
        self.redraw()

    def _on_task_deleted(self, task):
        if self.task == task:
            self.set_task(None)
            self.clear()
            ResultTab.instance().set_data([], [], [], [])

    def _on_tasks_list_updated(self):
        if not len(Global.tasks()):
            self.set_task(None)
            self.clear()
            ResultTab.instance().set_data([], [], [], [])

    @staticmethod
    def instance():
        return Plot.__instance

    def set_task(self, task):
        self.task = task

    def clear(self):
        self.figure.clf()
        self.figure.clear()
        gc.collect()

    def redraw(self):
        self.clear()

        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.grid(True)
        self.axes.set_xlabel('Phase')
        self.axes.set_ylabel('Flux')

        result_phases = []
        result_values = []
        import_phases = []
        import_values = []

        keys = sorted(self.task.result.data().keys())

        for key in keys:
            if self.task.result.data()[key]['result_value'] is not None:
                result_phases.append(key)
                result_values.append(self.task.result.data()[key]['result_value'])

            if self.task.result.data()[key]['import_value'] is not None:
                import_phases.append(key)
                import_values.append(self.task.result.data()[key]['import_value'])

        ResultTab.instance().set_data(result_phases, result_values, import_phases, import_values)

        if not result_phases and not import_phases :
            return

        y_r_min = 1
        y_r_max = 0
        x_r_max = 0
        y_i_min = 1
        y_i_max = 0
        x_i_max = 0

        if result_values :
            y_r_min = min(result_values)
            y_r_max = max(result_values)
            x_r_max = max(abs(min(result_phases)), abs(max(result_phases)))

        if import_values :
            y_i_min = min(import_values)
            y_i_max = max(import_values)
            x_i_max = max(abs(min(import_phases)), abs(max(import_phases)))

        y_max = max(y_r_max, y_i_max)
        y_min = min(y_r_min, y_i_min)
        x_max = max(x_r_max, x_i_max)
        y_pad = ((y_max - y_min) / 100) * 10
        x_pad = (x_max / 100) * 10

        if y_min == y_max:
            y_min += 1
            y_max -= 1

        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim([y_min - y_pad, y_max + y_pad])

        self.last_x_limit = [-(x_max + x_pad), x_max + x_pad]
        Global.event.plot_x_limit_changed.emit(self.last_x_limit)

        self.axes.set_autoscalex_on(False)
        self.axes.set_xlim(self.last_x_limit)

        if len(result_phases):
            self.axes.plot(result_phases, result_values, color='b', label="Prediction")

        if len(import_phases):
            self.axes.scatter(import_phases, import_values, s=1, color='r', label='Observation')

        self.draw()


class ResidualPlot(FigureCanvas):

    __instance = None

    def __init__(self):
        Global.event.task_selected.connect(self._on_task_selected)
        Global.event.plot_x_limit_changed.connect(self._on_x_limit_changed)
        Global.event.task_deleted.connect(self._on_task_deleted)
        Global.event.tasks_list_updated.connect(self._on_tasks_list_updated)

        self.task = None
        self.axes = None
        self.last_x_limit = []
        self.chi2s = []
        bg_color = str(QPalette().color(QPalette.Active, QPalette.Window).name())
        rcParams.update({'font.size': 10})

        self.figure = Figure(facecolor=bg_color, edgecolor=bg_color)
        self.figure.hold(False)
        super(ResidualPlot, self).__init__(self.figure)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.hide()

    def _on_task_selected(self, task):
        self.set_task(task)
        self.redraw()

    def _on_task_deleted(self, task):
        if self.task == task:
            self.set_task(None)
            self.clear()

    def _on_tasks_list_updated(self):
        if not len(Global.tasks()):
            self.set_task(None)
            self.clear()

    def set_task(self, task):
        self.task = task

    def clear(self):
        self.figure.clf()
        self.figure.clear()
        self.draw()
        self.parent().chi2_label.hide()
        self.parent().chi2_value.hide()
        self.hide()
        gc.collect()

    def redraw(self):
        self.clear()

        if self.task.result.chi2 is None:
            self.parent().chi2_label.hide()
            self.parent().chi2_value.hide()
            self.hide()
            return

        self.chi2s.append(self.task.result.chi2)

        self.show()
        self.parent().chi2_label.show()
        self.parent().chi2_value.show()

        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.grid(False)
        self.figure.set_alpha(0)
        self.axes.set_xlabel('Phase')
        self.axes.set_ylabel('Residual')

        phases = []
        delta_values = []

        keys = sorted(self.task.result.data().keys())

        for key in keys:
            if self.task.result.data()[key]['delta_value'] is not None:
                phases.append(key)
                delta_values.append(self.task.result.data()[key]['delta_value'])


        y_max = max(abs(min(delta_values)), abs(max(delta_values)))
        y_pad = (y_max / 100) * 10

        self.axes.set_autoscaley_on(False)
        self.axes.set_ylim([-(y_max + y_pad), y_max + y_pad])

        self.axes.set_autoscalex_on(False)
        self.axes.set_xlim(self.last_x_limit)

        color = QColor(0,0,0)
        min_chi2 = min(self.chi2s)
        if len(self.chi2s) == 1 :
            color = QColor(0,0,0)
        elif self.task.result.chi2 <= min_chi2 :
            color = QColor(0,139,0)
        else:
            color = QColor(255,0,0)

        self.axes.axhline(y=0, ls='--', linewidth=0.5, color='black')
        self.axes.scatter(phases, delta_values, s=0.5, color='r')

        palette = self.parent().chi2_value.palette()
        palette.setColor(QPalette.Active, QPalette.Text, color)
        self.parent().chi2_value.setPalette(palette)
        self.parent().chi2_value.setText(str(self.task.result.chi2))

        self.draw()

    def _on_x_limit_changed(self, limit):
        self.last_x_limit = limit


class ResultTab(QWidget):

    __instance = None

    def __init__(self):
        super(QWidget, self).__init__()

        if ResultTab.__instance is None :
            ResultTab.__instance = self

        self.phases = []
        self.values = []
        self.import_phases = []
        self.import_values = []

        self.export = None

        self.vl = QVBoxLayout()

        header = ['Phase', 'Synthetic', 'Observation', 'Delta']
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)

        self.vl.addWidget(self.table)

        hl = QHBoxLayout()
        hl.setAlignment(Qt.AlignRight)
        export_button = QPushButton('Export...')
        export_menu = QMenu()
        export_menu.addAction('\\t separated').triggered.connect(lambda : self._on_export('\t'))
        export_menu.addAction(', separated').triggered.connect(lambda : self._on_export(','))
        export_menu.addAction('; separated').triggered.connect(lambda : self._on_export(';'))
        export_button.setMenu(export_menu)
        hl.addWidget(export_button)

        self.vl.addLayout(hl)
        self.setLayout(self.vl)

    def set_data(self, phases, values, import_phases, import_values):

        self.phases = phases
        self.values = values
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

                value_item = QTableWidgetItem('%.12f' % import_values[import_index])
                value_item.setTextAlignment(Qt.AlignRight)

                delta_flux_item = QTableWidgetItem('%.12f' % (import_values[import_index] - self.values[index]))
                delta_flux_item.setTextAlignment(Qt.AlignRight)

                self.table.setItem(index, 2, value_item)
                self.table.setItem(index, 3, delta_flux_item)

    def _on_export(self, separator):
        self.export = ExportDatDialog(self.phases, self.values, self.import_phases, self.import_values, separator)
        pass

    @staticmethod
    def instance():
        return ResultTab.__instance


class ExportDatDialog(QFileDialog):

    def __init__(self, phases, values, import_phases, import_values, separator):
        super(ExportDatDialog, self).__init__()
        self.setWindowTitle('Export DAT')
        #self.setWindowIcon(QIcon('assets/export.png'))
        self.resize(500, 400)
        self.setFileMode(QFileDialog.AnyFile)
        filename = self.getSaveFileName(directory='result.dat', filter='DAT (*.dat);;')

        try:

            with open(filename, 'wb') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=separator)
                for index, phase in enumerate(phases):
                    row = []
                    row.append('%.12f' % phase)
                    row.append('%.12f' % values[index])

                    if phase in import_phases :
                        import_index = import_phases.index(phase)
                        row.append('%.12f' % import_values[import_index])
                        row.append('%.12f' % (import_values[import_index] - values[index]))

                    csv_writer.writerow(row)

        except:
            QMessageBox.warning(self, "Error", "Error exporting!\nError: " + str(sys.exc_info()[1]))
            raise


class ResultsTab(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        vl = QVBoxLayout()
        self.setLayout(vl)

        table = ResultsTable()
        vl.addWidget(table)

        hl = QHBoxLayout()
        hl.setAlignment(Qt.AlignRight)
        vl.addLayout(hl)

        delete_all_button = QPushButton('Delete all')
        delete_all_button.clicked.connect(self._on_delete_all_clicked)
        hl.addWidget(delete_all_button)

    def _on_delete_all_clicked(self):
        Global.event.interface_delete_all_results_clicked.emit()


class ResultsTable(QTableView):

    def __init__(self):
        QTableView.__init__(self)

        self.last_sort_column = 0
        self.last_sort_order = Qt.AscendingOrder
        self.last_selected_row = 0
        self.last_scroll_position = 0

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSortingEnabled(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setMovable(True)

        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(self._on_header_menu)

        self.doubleClicked.connect(self._on_row_double_clicked)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_row_menu)

        Global.event.tasks_list_updated.connect(self._on_tasks_list_updated)

    def keyPressEvent(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Delete:
            row = self.currentIndex().row()
            task = self.get_task_by_row(row)
            if task:
                self.delete_task_by_id(task.id)
        elif event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
            Global.event.task_selected.emit(self.get_task_by_row(self.currentIndex().row()))
        else:
            return QTableView.keyPressEvent(self, event)

    def _on_header_menu(self, point):
        menu = QMenu()
        for index, title in enumerate(self.model().header):
            action = QAction(self)
            action.setData(index)
            action.setText(title)
            action.setCheckable(True)
            action.setChecked(False if self.isColumnHidden(index) else True)
            action.triggered.connect(self._on_header_menu_action)

            menu.addAction(action)

        menu.popup(self.mapToGlobal(point))
        menu.exec_()

    def _on_header_menu_action(self, checked):
        index = self.sender().data().toInt()[0]
        if checked:
            self.showColumn(index)
        else:
            self.hideColumn(index)

    def _on_row_menu(self, point):
        row = self.rowAt(point.y())
        task = self.get_task_by_row(row)

        if row < 0 or task is None:
            return

        menu = QMenu()

        load_action = QAction(self)
        load_action.setData(task.id)
        load_action.setText("Load parameters")
        load_action.triggered.connect(self._on_load_params_action)
        menu.addAction(load_action)

        delete_action = QAction(self)
        delete_action.setData(task.id)
        delete_action.setText('Delete')
        delete_action.triggered.connect(self._on_row_delete_action)
        menu.addAction(delete_action)

        menu.popup(self.mapToGlobal(point))
        menu.exec_()

    def _on_load_params_action(self):
        id = self.sender().data().toInt()[0]
        Global.event.interface_load_task_params.emit(self.get_task_by_id(id))

    def _on_row_delete_action(self):
        id = self.sender().data().toInt()[0]
        self.delete_task_by_id(id)

    def delete_task_by_id(self, id):
        task = self.get_task_by_id(id)

        if task:
            Global.delete_task(task)

    def get_task_by_id(self, id):
        for task in self.model().tasks:
            if task.id == id:
                return task

        return None

    def get_task_by_row(self, row):
        if self.model() and -1 < row < len(self.model().tasks_data):
            return self.get_task_by_id(self.model().tasks_data[row][0])

        return None

    def _on_tasks_list_updated(self):
        if self.model():
            self.last_sort_column = self.model().last_sort_column
            self.last_sort_order = self.model().last_sort_order
            self.last_selected_row = self.currentIndex().row()
            self.last_scroll_position = self.verticalScrollBar().sliderPosition()

        self.setModel(ResultsTableModel(Global.tasks()))
        self.sortByColumn(self.last_sort_column, self.last_sort_order)
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        self.selectRow(self.last_selected_row)
        self.verticalScrollBar().setSliderPosition(self.last_scroll_position)

    def _on_row_double_clicked(self, index):
        target_id = self.model().tasks_data[index.row()][0]
        for task in self.model().tasks:
            if task.id == target_id:
                Global.event.task_selected.emit(task)
                break


class ResultsTableModel(QAbstractTableModel):

    def __init__(self, tasks):
        QAbstractTableModel.__init__(self)
        self.tasks = tasks
        self.tasks_data = []
        self.last_sort_column = 0
        self.last_sort_order = Qt.AscendingOrder
        self.header = ['#',
                        'Sma',
                        'Rs',
                        'Rp',
                        'Ts',
                        'Tp',
                        'Inc.',
                        'Darkening law',
                        'chi^2']

        for task in tasks:
            self.tasks_data.append([task.id,
                                    task.input.semi_major_axis,
                                    task.input.star_radius,
                                    task.input.planet_radius,
                                    task.input.star_temperature,
                                    task.input.planet_temperature,
                                    task.input.inclination,
                                    task.input.darkening_law + '(' + str(task.input.darkening_1) + ', ' + str(task.input.darkening_2) + ')',
                                    task.result.chi2])

    def rowCount(self, parent):
        return len(self.tasks_data)

    def columnCount(self, parent):
        return len(self.tasks_data[0]) if len(self.tasks_data) else 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.TextAlignmentRole:
            return QVariant(Qt.AlignRight | Qt.AlignVCenter)
        elif role != Qt.DisplayRole:
            return QVariant()

        return QVariant(self.tasks_data[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()

    def sort(self, col, order):
        self.last_sort_column = col
        self.last_sort_order = order

        self.layoutAboutToBeChanged.emit()
        self.tasks_data = sorted(self.tasks_data, key=operator.itemgetter(col))

        if order == Qt.DescendingOrder:
            self.tasks_data.reverse()

        self.layoutChanged.emit()