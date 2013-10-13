from copy import copy
import hashlib
from itertools import combinations
import md5
import marshal
from numpy import random
from PyQt4.QtCore import pyqtSignal, QObject, QThread
import time
from lib.Utils import mirror_phase_value_lists
from transitlib.transit import Transit as TransitLib


class GlobalEvent(QObject):
    # Tasks events
    task_created = pyqtSignal(object)
    task_selected = pyqtSignal(object)
    task_started = pyqtSignal(object)
    task_completed = pyqtSignal(object)
    task_progressed = pyqtSignal(object, int)
    task_stopped = pyqtSignal(object)
    task_deleted = pyqtSignal(object)
    tasks_list_updated = pyqtSignal()

    # Task range events
    task_range_changed = pyqtSignal(object)
    task_range_completed = pyqtSignal(object)
    task_range_progressed = pyqtSignal(int)

    # Plot events
    plot_x_limit_changed = pyqtSignal(list)

    # Interface events
    interface_redraw_clicked = pyqtSignal()
    interface_calculate_clicked = pyqtSignal()
    interface_auto_plot_state_changed = pyqtSignal(bool)
    interface_delete_all_results_clicked = pyqtSignal()
    interface_load_task_params = pyqtSignal(object)

    # Other events
    data_imported = pyqtSignal(list, list)

    def __init__(self):
        QObject.__init__(self)
        pass


class Global:

    _task = None
    _task_range = None
    _tasks = []
    _auto_plot = False
    event = GlobalEvent()

    def __init__(self):
        pass

    @staticmethod
    def init():
        Global.create_task()
        Global._task_range = TaskRange()
        Global.event.task_completed.connect(Global._on_task_completed)
        Global.event.task_stopped.connect(Global._on_task_stopped)
        Global.event.task_range_completed.connect(Global._on_task_range_completed)
        Global.event.data_imported.connect(Global._on_data_imported)
        Global.event.interface_redraw_clicked.connect(Global._on_interface_redraw_clicked)
        Global.event.interface_auto_plot_state_changed.connect(Global._on_interface_auto_plot_state_changed)
        Global.event.interface_delete_all_results_clicked.connect(Global._on_interface_delete_all_results_clicked)

    @staticmethod
    def _on_task_completed(task):
        Global._tasks.append(task)
        Global.event.tasks_list_updated.emit()
        Global.create_task()

        if len(Global.tasks()) == 1 or Global._auto_plot:
            Global.event.task_selected.emit(task)

        if Global.task_range().total_count():
            if not Global.task_range().uncompleted_count():
                Global.event.task_range_completed.emit(Global.task_range())
            else:
                Global.event.task_range_progressed.emit((float(Global.task_range().completed_count()-1)/Global.task_range().total_count())*100)

    @staticmethod
    def _on_task_stopped(task):
        Global.create_task()
        Global.task_range().reset_iterator()

    @staticmethod
    def _on_task_range_completed():
        Global.task_range().reset_iterator()

    @staticmethod
    def _on_data_imported(phases, values):
        Global.task().input.phases_injection = phases
        Global.task().result.set_import(phases, values)

    @staticmethod
    def _on_interface_redraw_clicked():
        Global.event.task_selected.emit(Global.task())

    @staticmethod
    def _on_interface_auto_plot_state_changed(checked):
        Global._auto_plot = checked

    @staticmethod
    def _on_interface_delete_all_results_clicked():
        Global._tasks = []
        Global.event.tasks_list_updated.emit()

    @staticmethod
    def tasks():
        return Global._tasks

    @staticmethod
    def task():
        """
        :rtype: Task
        """
        return Global._task

    @staticmethod
    def task_range():
        """
        :rtype: TaskRange
        """
        return Global._task_range

    @staticmethod
    def delete_task(task):
        for index, t in enumerate(Global.tasks()):
            if t == task:
                del Global._tasks[index]
                Global.event.tasks_list_updated.emit()
                Global.event.task_deleted.emit(task)

                if task == Global.task():
                    Global.create_task()

    @staticmethod
    def create_task():
        Global._task = Task()
        Global.event.task_created.emit(Global._task)

    @staticmethod
    def auto_plot():
        return Global._auto_plot

class TaskResult(QObject):

    def __init__(self):
        super(TaskResult, self).__init__()
        self._data = {}
        self._frozen = False
        self._freeze_filename = ''
        self.chi2 = None

    def set_result(self, phases, values):
        phases, values = mirror_phase_value_lists(phases, values)
        self._put_data(phases, values, 'result_value')

        for key in self.data():
            data = self.data()[key]
            if data['result_value'] and data['import_value']:
                self.chi2 = float(0) if self.chi2 is None else self.chi2
                self.chi2 += data['delta_value'] ** 2

    def _put_data(self, phases, values, key):

        for index, phase in enumerate(phases):
            if not self.data().has_key(phase):
                self.data()[phase] = {'result_value': None, 'import_value': None, 'delta_value': None}

            self.data()[phase][key] = values[index]

            if self.data()[phase]['result_value'] is not None and self.data()[phase]['import_value'] is not None:
                self.data()[phase]['delta_value'] = self.data()[phase]['import_value'] - self.data()[phase]['result_value']

    def set_import(self, phases, values):
        self._data = {}
        self._frozen = False
        self._put_data(phases, values, 'import_value')
        pass

    def freeze(self):
        if not self._freeze_filename:
            md5_hash = hashlib.md5()
            md5_hash.update(str(time.time()) + str(random.random()))
            self._freeze_filename = './config/temp/task_freeze_' + str(md5_hash.hexdigest())

        dump_file = open(self._freeze_filename, 'wb')
        marshal.dump(self._data, dump_file)
        dump_file.close()
        self._data = None
        self._frozen = True

    def frozen(self):
        return self._frozen

    def data(self):
        """
        :rtype: dict
        """
        if self._frozen:
            dump_file = open(self._freeze_filename, 'rb')
            self._data = dict(marshal.load(dump_file))
            dump_file.close()
            self._frozen = False
            pass

        return self._data


class Task(QObject):

    _next_task_id = 1

    def __init__(self):
        super(Task, self).__init__()
        self.id = Task._next_task_id
        Task._next_task_id += 1
        self.thread = Transit()
        self.input = TaskInput()
        self.result = TaskResult()
        self.completed = False
        self.canceled = False
        Global.event.task_selected.connect(self._on_task_selected)
        pass

    def start(self):
        self.thread.set_semi_major_axis(self.input.semi_major_axis)
        self.thread.set_star_radius(self.input.star_radius)
        self.thread.set_planet_radius(self.input.planet_radius)
        self.thread.set_star_temperature(self.input.star_temperature)
        self.thread.set_planet_temperature(self.input.planet_temperature)
        self.thread.set_inclination(self.input.inclination)
        self.thread.set_star_darkening_type(self.input.darkening_law)
        self.thread.set_star_darkening_1(self.input.darkening_1)
        self.thread.set_star_darkening_2(self.input.darkening_2)
        self.thread.set_phase_start(self.input.phase_start)
        self.thread.set_phase_end(self.input.phase_end)
        self.thread.set_phase_step(self.input.phase_step)
        self.thread.set_precision(self.input.precision)
        self.thread.set_phases_injection(self.input.phases_injection)

        self.thread.event.progress.connect(self._on_progressed)
        self.thread.event.complete.connect(self._on_completed)
        self.thread.event.stop.connect(self._on_stopped)

        self.thread.start()
        Global.event.task_started.emit(self)

    def _on_progressed(self, progress):
        Global.event.task_progressed.emit(self, progress)

    def _on_completed(self, result):
        self.result.set_result(result.phases, result.values)
        self.completed = True
        Global.event.task_completed.emit(self)
        self.result.freeze()

    def _on_stopped(self):
        self.completed = True
        self.canceled = True
        Global.event.task_stopped.emit(self)

    def _on_task_selected(self, task):
        if task != self and self.completed and self.result.frozen() == False:
            self.result.freeze()

    def stop(self):
        if self.thread:
            self.thread.stop()


class TaskInput(object):

    def __init__(self):
        self.semi_major_axis = float(0.0)
        self.star_radius = float(0.0)
        self.planet_radius = float(0.0)
        self.star_temperature = float(0.0)
        self.planet_temperature = float(0.0)
        self.inclination = float(0.0)
        self.darkening_law = None
        self.darkening_1 = float(0.0)
        self.darkening_2 = float(0.0)
        self.phase_start = float(0.0)
        self.phase_end = float(0.0)
        self.phase_step = float(0.0)
        self.precision = 0
        self.phases_injection = []
        pass


class TaskRange:

    def __init__(self):
        self.ranges = []
        self.params = set()
        self.combinations = []
        self._total_count = 0
        self._completed_count = 0
        Global.event.task_completed.connect(self._on_task_completed)

    def _on_task_completed(self, task):
        self._completed_count += 1

    def set_range(self, name, values):
        for value in values:
            self.ranges.append([name, value])

        self.params.add(name)
        self._total_count = max(self._total_count, 1) * len(values)
        self.reset_iterator()

    @staticmethod
    def _find_combinations(iterable, r):
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = range(r)

        if r == 1:
            yield tuple(pool[i] for i in indices)

        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1

            keys = []
            for i in indices:
                keys.append(pool[i][0])

            if len(set(keys)) != r:
                continue

            yield tuple(pool[i] for i in indices)

    def get_next_combination(self):
        try:
            return self.combinations.next()
        except:
            return None

    def reset(self):
        self.ranges = []
        self.params = set()
        self._total_count = 0
        self.combinations = []
        self.reset_iterator()

    def reset_iterator(self):
        self._completed_count = 0
        self.combinations = TaskRange._find_combinations(self.ranges, len(self.params))

    def total_count(self):
        return self._total_count

    def completed_count(self):
        return self._completed_count

    def uncompleted_count(self):
        return self._total_count - self._completed_count


class TransitResult(QObject):

    def __init__(self):
        super(TransitResult, self).__init__()
        self.phases = []
        self.values = []


class TransitEvent(QObject):

    progress = pyqtSignal(int)
    complete = pyqtSignal(object)
    stop     = pyqtSignal()


class Transit(TransitLib, QThread):

    event = TransitEvent()

    def __init__(self):
        super(Transit, self).__init__()
        self.event = TransitEvent()

    def onStop(self):
        self.event.stop.emit()
        Transit.event.stop.emit()
        pass

    def onProgress(self, progress):
        self.event.progress.emit(progress)
        Transit.event.progress.emit(progress)
        pass

    def onComplete(self, phases, values):
        result = TransitResult()
        result.phases = phases
        result.values = values
        self.event.complete.emit(result)
        Transit.event.complete.emit(result)
        pass