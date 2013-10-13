import re
from PyQt4.QtCore import QObject


import logging

FORMAT = "%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
FORMAT = "%(message)s %(levelname)s %(pathname)s %(lineno)d"

logger = logging.getLogger('mainlog')

def frange(start, end=None, inc=None):
    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L


def flip_phase_list(phases):
    for index, phase in enumerate(phases):
        phases[index] = phase if phase <= 0.5 else phase - 1

    return phases


def mirror_phase_value_lists(phases, values):
    new_phases = []
    for phase in phases:
        new_phases.append(phase * -1)

    return new_phases + phases, values + values


def uc_variable_name(s):
    return "".join([w[0].upper() + w[1:] for w in re.split('_', s)])


def add_triplet(container, triplet, position):
    container.addWidget(triplet.label, position, 0)
    container.addWidget(triplet.value, position, 1)
    container.addWidget(triplet.unit, position, 2)
    return triplet


class Constants:

    SUN_RADIUS = 6.955*10**8
    JUPITER_RADIUS = 6.9173*10**7
    AU = 149597870691.0

    @staticmethod
    def au_to_rs(value):
        return (value * Constants.AU) / Constants.SUN_RADIUS

    @staticmethod
    def rs_to_au(value):
        return value * Constants.SUN_RADIUS / Constants.AU

    @staticmethod
    def au_to_rj(value):
        return (value * Constants.AU) / Constants.JUPITER_RADIUS

    @staticmethod
    def rj_to_au(value):
        return value * Constants.JUPITER_RADIUS / Constants.AU


class TaskImporter(QObject):

    @staticmethod
    def load_file(filename):
        phases = []
        values = []

        with open(filename, 'rb') as csvfile:
            for line in csvfile.readlines():
                m = re.search('(-?\d+\.\d+)(\D+?)(-?\d+\.\d+)', line)

                if not m is None:
                    phases.append(float(m.group(1)))
                    values.append(float(m.group(3)))

        return phases, values

    @staticmethod
    def get_formats():
        return ['dat', 'csv']