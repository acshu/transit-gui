from _ast import List
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDoubleSpinBox, QLabel, QWidget, QComboBox, QFont, QFrame, QCheckBox
from matplotlib.backends.qt4_editor.formlayout import QPushButton, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout
from lib.Utils import frange, Constants, add_triplet


class CustomDoubleSpinBox(QDoubleSpinBox):

    def __init__(self, parent=None, value=0):
        super(CustomDoubleSpinBox, self).__init__(parent)

    def textFromValue(self, value):
        result = str(QDoubleSpinBox.textFromValue(self, value))
        if result.find(".") > 0:
            result = result.rstrip("0")
            result = result.rstrip(".")
        return result


class RangeButton(QPushButton):

    state_changed = pyqtSignal(bool)
    TYPE_STEP = 'range-step'
    TYPE_VALUES = 'range-values'

    def __init__(self):
        QPushButton.__init__(self)
        self.setText('R')
        font = QFont()
        font.setPixelSize(8)
        self.setFont(font)
        self.setFixedSize(18, 18)
        self.range_type = None
        self.range_from = None
        self.range_to = None
        self.range_step = None
        self.values = []
        self._active = False

    def set_range(self, range_from, range_to=None, range_step=None):
        if type(range_from) is list:
            self.values = range_from
            self.range_type = RangeButton.TYPE_VALUES
        else:
            self.range_from = range_from
            self.range_to = range_to
            self.range_step = range_step
            self.range_type = RangeButton.TYPE_STEP
            self.values = frange(range_from, range_to, range_step) + [range_to]

    def set_active(self, bool):
        self._active = bool
        self.setCheckable(bool)
        self.setChecked(bool)
        self.state_changed.emit(bool)

    def is_active(self):
        return self._active


class Triplet(QWidget):

    def __init__(self, label, value, unit='', range=False):
        QWidget.__init__(self)
        self.label = QLabel(label)
        self.value = value
        self.unit = QLabel(unit)
        self.range = RangeButton()

        if not range:
            self.range.setVisible(False)

    def getValue(self):
        return self.value.value()

    def setDisabled(self, bool):
        QWidget.setDisabled(self, bool)
        self.label.setDisabled(bool)
        self.value.setDisabled(bool)
        self.unit.setDisabled(bool)


class SemiMajorAxis(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Semi-major axis:', CustomDoubleSpinBox(), 'AU', True)

        self.value.setRange(0, 9999)
        self.value.setSingleStep(0.001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(1)


class SemiMajorAxisStep(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'By:', CustomDoubleSpinBox(), 'AU', True)

        self.value.setRange(0, 9999)
        self.value.setSingleStep(0.001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.001)


class StarRadiusAU(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Star radius:', CustomDoubleSpinBox(), 'AU', True);

        self.value.setRange(0, 9999999999)
        self.value.setSingleStep(0.0001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.00364026905)


class StarRadiusRS(Triplet):

    def __init__(self):
        Triplet.__init__(self, '', CustomDoubleSpinBox(), 'R<small>sun</small>');

        self.value.setRange(0, 9999999999)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)


class StarRadiusStepAU(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'By:', CustomDoubleSpinBox(), 'AU')

        self.value.setRange(0, 1)
        self.value.setSingleStep(0.001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.001)


class StarRadiusStepRS(Triplet):

    def __init__(self):
        Triplet.__init__(self, '', CustomDoubleSpinBox(), 'R<small>sun</small>')

        self.value.setRange(0, 1000)
        self.value.setSingleStep(0.001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.001)


class PlanetRadiusAU(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Planet radius:', CustomDoubleSpinBox(), 'AU', True)

        self.value.setRange(0, 9999)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(1) # 0.00050471226


class PlanetRadiusStepAU(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'By:', CustomDoubleSpinBox(), 'AU')

        self.value.setRange(0, 1)
        self.value.setSingleStep(0.001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.001)

class PlanetRadiusStepRJ(Triplet):

    def __init__(self):
        Triplet.__init__(self, '', CustomDoubleSpinBox(), 'R<small>jup</small>')

        self.value.setRange(0, 1000)
        self.value.setSingleStep(0.001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.001)


class PlanetRadiusRJ(Triplet):

    def __init__(self):
        Triplet.__init__(self, '', CustomDoubleSpinBox(), 'R<small>jup</small>')

        self.value.setRange(0, 9999999999)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)


class StarTemperature(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Star temperature:', CustomDoubleSpinBox(), 'K', True)

        self.value = CustomDoubleSpinBox()
        self.value.setRange(0, 99999)
        self.value.setSingleStep(1)
        self.value.setDecimals(0)
        self.value.setAccelerated(True)
        self.value.setValue(4675)


class StarTemperatureStep(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'By:', CustomDoubleSpinBox(), 'K')

        self.value = CustomDoubleSpinBox()
        self.value.setRange(0, 99999)
        self.value.setSingleStep(1)
        self.value.setDecimals(0)
        self.value.setAccelerated(True)
        self.value.setValue(100)


class PlanetTemperature(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Planet temperature:', CustomDoubleSpinBox(), 'K', True)

        self.value.setRange(0, 99999)
        self.value.setSingleStep(1)
        self.value.setDecimals(0)
        self.value.setAccelerated(True)
        self.value.setValue(1300)


class PlanetTemperatureStep(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'By:', CustomDoubleSpinBox(), 'K')

        self.value.setRange(0, 99999)
        self.value.setSingleStep(1)
        self.value.setDecimals(0)
        self.value.setAccelerated(True)
        self.value.setValue(10)


class Inclination(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Inclination:', CustomDoubleSpinBox(), 'Deg', True)

        self.value.setRange(0, 90)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(90) # 86.80


class InclinationStep(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'By:', CustomDoubleSpinBox(), '')

        self.value.setRange(0, 1)
        self.value.setSingleStep(0.001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.001) # 86.80


class DarkeningLaw(Triplet):

    items = ('Linear', 'linear'), ('Quadratic', 'quadratic'), ('Square root', 'squareroot'), ('Logarithmic', 'logarithmic')

    def __init__(self):
        Triplet.__init__(self, 'Darkening law:', QComboBox(), '', True)

        self.value = QComboBox()
        for item in self.items:
            self.value.addItem(item[0], item[1])


class DarkeningCoefficient(Triplet):

    def __init__(self, label='', unit=''):
        Triplet.__init__(self, label, CustomDoubleSpinBox(), unit, True)

        self.value.setRange(0, 1)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0)

class DarkeningCoefficientStep(Triplet):

    def __init__(self, unit=''):
        Triplet.__init__(self, 'By:', CustomDoubleSpinBox(), unit, True)

        self.value.setRange(0, 1)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.01)


class PhaseEnd(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Phase end:', CustomDoubleSpinBox(), '')

        self.value.setRange(0, 0.5)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.2)


class PhaseStep(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Phase step:', CustomDoubleSpinBox(), '')

        self.value.setRange(0, 1)
        self.value.setSingleStep(0.00001)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0.0001)


class IntegrationPrecision(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Precision 10^?:', CustomDoubleSpinBox(), '')

        self.value.setDecimals(0)
        self.value.setRange(-10, 0)
        self.value.setValue(-1)


class RangeDialog(QDialog):

    def __init__(self, title):
        QDialog.__init__(self, None, Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.setFixedWidth(220)
        self.setWindowTitle(title)
        self.setModal(True)

        self.ok_button = QPushButton('OK')
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)

        frame = QFrame();
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setFixedHeight(10)

        hl = QHBoxLayout()
        hl.addWidget(self.ok_button, 1, Qt.AlignLeft)
        hl.addWidget(self.cancel_button, 0, Qt.AlignRight)

        vl = QVBoxLayout()
        vl.addWidget(frame)
        vl.addLayout(hl)

        self.setLayout(vl)

    def display(self):
        self.exec_()


class InclinationRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Inclination range')

        self.setFixedHeight(140)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        grid.setColumnMinimumWidth(0,60)


        self.inclination_from = Inclination()
        self.inclination_from.label.setText('From:')
        range_from = 85 if not range_from else range_from
        self.inclination_from.value.setValue(range_from)

        self.inclination_to = Inclination()
        self.inclination_to.label.setText('To:')
        range_to = 90 if not range_to else range_to
        self.inclination_to.value.setValue(range_to)

        self.inclination_step = InclinationStep()
        range_step = self.inclination_step.value.value() if not range_step else range_step
        self.inclination_step.value.setValue(range_step)

        add_triplet(grid, self.inclination_from, 1)
        add_triplet(grid, self.inclination_to, 2)
        add_triplet(grid, self.inclination_step, 3)

        self.layout().insertLayout(0, grid)


class PlanetRadiusRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Planet radius range')
        self.setFixedHeight(222)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        grid.setColumnMinimumWidth(0,60)

        self.planet_radius_from = PlanetRadiusAU()
        self.planet_radius_from.label.setText('From:')
        self.planet_radius_from_rj = PlanetRadiusRJ()

        self.planet_radius_to = PlanetRadiusAU()
        self.planet_radius_to.label.setText('To:')
        self.planet_radius_to_rj = PlanetRadiusRJ()

        self.planet_radius_step = PlanetRadiusStepAU()
        self.planet_radius_step_rj = PlanetRadiusStepRJ()


        self.planet_radius_from.value.valueChanged.connect(self._on_au_change)
        self.planet_radius_to.value.valueChanged.connect(self._on_au_change)
        self.planet_radius_step.value.valueChanged.connect(self._on_au_change)

        self.planet_radius_from_rj.value.valueChanged.connect(self._on_rj_change)
        self.planet_radius_to_rj.value.valueChanged.connect(self._on_rj_change)
        self.planet_radius_step_rj.value.valueChanged.connect(self._on_rj_change)

        self.planet_radius_from.value.setValue(0 if not range_from else range_from)
        self.planet_radius_to.value.setValue(1 if not range_to else range_to)
        self.planet_radius_step.value.setValue(0.001 if not range_step else range_step)

        add_triplet(grid, self.planet_radius_from, 1)
        add_triplet(grid, self.planet_radius_from_rj, 2)

        add_triplet(grid, self.planet_radius_to, 3)
        add_triplet(grid, self.planet_radius_to_rj, 4)

        add_triplet(grid, self.planet_radius_step, 5)
        add_triplet(grid, self.planet_radius_step_rj, 6)

        self.layout().insertLayout(0, grid)

    def _on_au_change(self, value):
        target = None

        if self.sender() == self.planet_radius_from.value:
            target = self.planet_radius_from_rj
        elif self.sender() == self.planet_radius_to.value:
            target = self.planet_radius_to_rj
        elif self.sender() == self.planet_radius_step.value:
            target = self.planet_radius_step_rj

        if target:
            target.value.blockSignals(True)
            target.value.setValue(Constants.au_to_rj(value))
            target.value.blockSignals(False)

    def _on_rj_change(self, value):
        target = None

        if self.sender() == self.planet_radius_from_rj.value:
            target = self.planet_radius_from
        elif self.sender() == self.planet_radius_to_rj.value:
            target = self.planet_radius_to
        elif self.sender() == self.planet_radius_step_rj.value:
            target = self.planet_radius_step

        if target:
            target.value.blockSignals(True)
            target.value.setValue(Constants.rj_to_au(value))
            target.value.blockSignals(False)


class SemiMajorAxisRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Semi-major axis range')

        self.setFixedHeight(140)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        grid.setColumnMinimumWidth(0,60)


        self.semi_major_axis_from = SemiMajorAxis()
        self.semi_major_axis_from.label.setText('From:')
        range_from = 0.001 if not range_from else range_from
        self.semi_major_axis_from.value.setValue(range_from)

        self.semi_major_axis_to = SemiMajorAxis()
        self.semi_major_axis_to.label.setText('To:')
        range_to = 2 if not range_to else range_to
        self.semi_major_axis_to.value.setValue(range_to)

        self.semi_major_axis_step = SemiMajorAxisStep()
        range_step = self.semi_major_axis_step.value.value() if not range_step else range_step
        self.semi_major_axis_step.value.setValue(range_step)

        add_triplet(grid, self.semi_major_axis_from, 1)
        add_triplet(grid, self.semi_major_axis_to, 2)
        add_triplet(grid, self.semi_major_axis_step, 3)

        self.layout().insertLayout(0, grid)


class StarRadiusRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Star radius range')
        self.setFixedHeight(222)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        grid.setColumnMinimumWidth(0,60)

        self.star_radius_from = StarRadiusAU()
        self.star_radius_from.label.setText('From:')
        self.star_radius_from_rs = StarRadiusRS()

        self.star_radius_to = StarRadiusAU()
        self.star_radius_to.label.setText('To:')
        self.star_radius_to_rs = PlanetRadiusRJ()

        self.star_radius_step = StarRadiusStepAU()
        self.star_radius_step_rs = StarRadiusStepRS()

        self.star_radius_from.value.valueChanged.connect(self._on_au_change)
        self.star_radius_to.value.valueChanged.connect(self._on_au_change)
        self.star_radius_step.value.valueChanged.connect(self._on_au_change)

        self.star_radius_from_rs.value.valueChanged.connect(self._on_rs_change)
        self.star_radius_to_rs.value.valueChanged.connect(self._on_rs_change)
        self.star_radius_step_rs.value.valueChanged.connect(self._on_rs_change)

        self.star_radius_from.value.setValue(0 if not range_from else range_from)
        self.star_radius_to.value.setValue(1 if not range_to else range_to)
        self.star_radius_step.value.setValue(0.001 if not range_step else range_step)

        add_triplet(grid, self.star_radius_from, 1)
        add_triplet(grid, self.star_radius_from_rs, 2)

        add_triplet(grid, self.star_radius_to, 3)
        add_triplet(grid, self.star_radius_to_rs, 4)

        add_triplet(grid, self.star_radius_step, 5)
        add_triplet(grid, self.star_radius_step_rs, 6)

        self.layout().insertLayout(0, grid)

    def _on_au_change(self, value):
        target = None

        if self.sender() == self.star_radius_from.value:
            target = self.star_radius_from_rs
        elif self.sender() == self.star_radius_to.value:
            target = self.star_radius_to_rs
        elif self.sender() == self.star_radius_step.value:
            target = self.star_radius_step_rs

        if target:
            target.value.blockSignals(True)
            target.value.setValue(Constants.au_to_rs(value))
            target.value.blockSignals(False)

    def _on_rs_change(self, value):
        target = None

        if self.sender() == self.star_radius_from_rs.value:
            target = self.star_radius_from
        elif self.sender() == self.star_radius_to_rs.value:
            target = self.star_radius_to
        elif self.sender() == self.star_radius_step_rs.value:
            target = self.star_radius_step

        if target:
            target.value.blockSignals(True)
            target.value.setValue(Constants.rs_to_au(value))
            target.value.blockSignals(False)


class DarkeningLawRangeDialog(RangeDialog):

    def __init__(self, values=None):
        RangeDialog.__init__(self, 'Darkening law range')
        self.setFixedHeight(102)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)

        self.checkboxes = []

        row = 1
        cell = 1
        for item in DarkeningLaw.items:
            checkbox = QCheckBox(item[0])
            checkbox.setObjectName(item[1])
            checkbox.stateChanged.connect(self._on_checkbox_state_changed)
            grid.addWidget(checkbox, row, cell)
            self.checkboxes.append(checkbox)

            if values and item[1] in values:
                checkbox.setChecked(True)

            cell += 1

            if cell > 2:
                cell = 1
                row += 1

        self.layout().insertLayout(0, grid)

        if not len(self.values()):
            self.ok_button.setDisabled(True)

    def _on_checkbox_state_changed(self):
        if not len(self.values()):
            self.ok_button.setDisabled(True)
        else:
            self.ok_button.setDisabled(False)

    def values(self):
        checked = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                checked.append(str(checkbox.objectName()))

        return checked


class DarkeningCoefficient1RangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Darkening coefficient 1 range')

        self.setFixedHeight(140)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        grid.setColumnMinimumWidth(0,60)

        self.darkening_coefficient_1_from = DarkeningCoefficient()
        self.darkening_coefficient_1_from.label.setText('From:')
        range_from = 0 if not range_from else range_from
        self.darkening_coefficient_1_from.value.setValue(range_from)

        self.darkening_coefficient_1_to = DarkeningCoefficient()
        self.darkening_coefficient_1_to.label.setText('To:')
        range_to = 1 if not range_to else range_to
        self.darkening_coefficient_1_to.value.setValue(range_to)

        self.darkening_coefficient_1_step = DarkeningCoefficientStep()
        range_step = self.darkening_coefficient_1_step.value.value() if not range_step else range_step
        self.darkening_coefficient_1_step.value.setValue(range_step)

        add_triplet(grid, self.darkening_coefficient_1_from, 1)
        add_triplet(grid, self.darkening_coefficient_1_to, 2)
        add_triplet(grid, self.darkening_coefficient_1_step, 3)

        self.layout().insertLayout(0, grid)


class DarkeningCoefficient2RangeDialog(DarkeningCoefficient1RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        DarkeningCoefficient1RangeDialog.__init__(self, range_from, range_to, range_step)
        self.setWindowTitle('Darkening coefficient 2 range')
        self.darkening_coefficient_2_from = self.darkening_coefficient_1_from
        self.darkening_coefficient_2_to = self.darkening_coefficient_1_to
        self.darkening_coefficient_2_step = self.darkening_coefficient_1_step


class StarTemperatureRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Star temperature range')

        self.setFixedHeight(140)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        grid.setColumnMinimumWidth(0,60)

        self.star_temperature_from = StarTemperature()
        self.star_temperature_from.label.setText('From:')
        range_from = 2000 if not range_from else range_from
        self.star_temperature_from.value.setValue(range_from)

        self.star_temperature_to = StarTemperature()
        self.star_temperature_to.label.setText('To:')
        range_to = 10000 if not range_to else range_to
        self.star_temperature_to.value.setValue(range_to)

        self.star_temperature_step = StarTemperatureStep()
        range_step = self.star_temperature_step.value.value() if not range_step else range_step
        self.star_temperature_step.value.setValue(range_step)

        add_triplet(grid, self.star_temperature_from, 1)
        add_triplet(grid, self.star_temperature_to, 2)
        add_triplet(grid, self.star_temperature_step, 3)

        self.layout().insertLayout(0, grid)


class PlanetTemperatureRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Planet temperature range')

        self.setFixedHeight(140)

        grid = QGridLayout()
        grid.setAlignment(Qt.AlignTop)
        grid.setColumnStretch(1,1)
        grid.setColumnMinimumWidth(0,60)

        self.planet_temperature_from = PlanetTemperature()
        self.planet_temperature_from.label.setText('From:')
        range_from = 0 if not range_from else range_from
        self.planet_temperature_from.value.setValue(range_from)

        self.planet_temperature_to = PlanetTemperature()
        self.planet_temperature_to.label.setText('To:')
        range_to = 1000 if not range_to else range_to
        self.planet_temperature_to.value.setValue(range_to)

        self.planet_temperature_step = PlanetTemperatureStep()
        range_step = self.planet_temperature_step.value.value() if not range_step else range_step
        self.planet_temperature_step.value.setValue(range_step)

        add_triplet(grid, self.planet_temperature_from, 1)
        add_triplet(grid, self.planet_temperature_to, 2)
        add_triplet(grid, self.planet_temperature_step, 3)

        self.layout().insertLayout(0, grid)