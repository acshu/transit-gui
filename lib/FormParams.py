from _ast import List
from PyQt4.QtCore import Qt, pyqtSignal
from PyQt4.QtGui import QDoubleSpinBox, QLabel, QWidget, QComboBox, QFont, QGroupBox, QTextEdit, QFrame
from matplotlib.backends.qt4_editor.formlayout import QPushButton, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit
from lib.Utils import frange, Constants


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

    def __init__(self):
        QPushButton.__init__(self)
        self.setText('R')
        font = QFont()
        font.setPixelSize(8)
        self.setFont(font)
        self.setFixedSize(16,16)
        self.range_from = None
        self.range_to = None
        self.range_step = None
        self.values = []
        self._active = False

    def set_range(self, range_from, range_to=None, range_step=None):
        if type(range_from) is list:
            self.values = range_from
        else:
            self.range_from = range_from
            self.range_to = range_to
            self.range_step = range_step
            self.values = frange(range_from, range_to, range_step) + [range_to]

        print self.values

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
        Triplet.__init__(self, 'Star temperature:', CustomDoubleSpinBox(), 'K')

        self.value = CustomDoubleSpinBox()
        self.value.setRange(0, 99999)
        self.value.setSingleStep(1)
        self.value.setDecimals(0)
        self.value.setAccelerated(True)
        self.value.setValue(4675)


class PlanetTemperature(Triplet):

    def __init__(self):
        Triplet.__init__(self, 'Planet temperature:', CustomDoubleSpinBox(), 'K')

        self.value.setRange(0, 99999)
        self.value.setSingleStep(1)
        self.value.setDecimals(0)
        self.value.setAccelerated(True)
        self.value.setValue(1300)


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

    def __init__(self):
        Triplet.__init__(self, 'Darkening law:', QComboBox(), '')

        self.value = QComboBox()
        self.value.addItem('Linear', 'linear')
        self.value.addItem('Quadratic', 'quadratic')
        self.value.addItem('Square root', 'squareroot')
        self.value.addItem('Logarithmic', 'logarithmic')


class DarkeningCoefficient(Triplet):

    def __init__(self, label='', unit=''):
        Triplet.__init__(self, label, CustomDoubleSpinBox(), unit)

        self.value.setRange(0, 1)
        self.value.setSingleStep(0.01)
        self.value.setDecimals(10)
        self.value.setAccelerated(True)
        self.value.setValue(0)
        self.value.setRange(-9999,9999)


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

        ok_button = QPushButton('OK')
        ok_button.setDefault(True)
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)

        frame = QFrame();
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        frame.setFixedHeight(10)

        hl = QHBoxLayout()
        hl.addWidget(ok_button, 1, Qt.AlignLeft)
        hl.addWidget(cancel_button, 0, Qt.AlignRight)

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

        self.add_triplet(grid, self.inclination_from, 1)
        self.add_triplet(grid, self.inclination_to, 2)
        self.add_triplet(grid, self.inclination_step, 3)

        self.layout().insertLayout(0, grid)


    @staticmethod
    def add_triplet(container, triplet, position):
        container.addWidget(triplet.label, position, 0)
        container.addWidget(triplet.value, position, 1)
        container.addWidget(triplet.unit, position, 2)
        return triplet


class PlanetRadiusRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Planet radius range')
        self.setFixedHeight(222)

        self._changeFromSignal = False

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

        self.add_triplet(grid, self.planet_radius_from, 1)
        self.add_triplet(grid, self.planet_radius_from_rj, 2)

        self.add_triplet(grid, self.planet_radius_to, 3)
        self.add_triplet(grid, self.planet_radius_to_rj, 4)

        self.add_triplet(grid, self.planet_radius_step, 5)
        self.add_triplet(grid, self.planet_radius_step_rj, 6)

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


    @staticmethod
    def add_triplet(container, triplet, position):
        container.addWidget(triplet.label, position, 0)
        container.addWidget(triplet.value, position, 1)
        container.addWidget(triplet.unit, position, 2)
        return triplet


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

        self.add_triplet(grid, self.semi_major_axis_from, 1)
        self.add_triplet(grid, self.semi_major_axis_to, 2)
        self.add_triplet(grid, self.semi_major_axis_step, 3)

        self.layout().insertLayout(0, grid)

    @staticmethod
    def add_triplet(container, triplet, position):
        container.addWidget(triplet.label, position, 0)
        container.addWidget(triplet.value, position, 1)
        container.addWidget(triplet.unit, position, 2)
        return triplet


class StarRadiusRangeDialog(RangeDialog):

    def __init__(self, range_from=None, range_to=None, range_step=None):
        RangeDialog.__init__(self, 'Star radius range')
        self.setFixedHeight(222)

        self._changeFromSignal = False

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

        self.add_triplet(grid, self.star_radius_from, 1)
        self.add_triplet(grid, self.star_radius_from_rs, 2)

        self.add_triplet(grid, self.star_radius_to, 3)
        self.add_triplet(grid, self.star_radius_to_rs, 4)

        self.add_triplet(grid, self.star_radius_step, 5)
        self.add_triplet(grid, self.star_radius_step_rs, 6)

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


    @staticmethod
    def add_triplet(container, triplet, position):
        container.addWidget(triplet.label, position, 0)
        container.addWidget(triplet.value, position, 1)
        container.addWidget(triplet.unit, position, 2)
        return triplet