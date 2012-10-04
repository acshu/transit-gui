# -*- coding: utf-8 -*-

import csv
from Transit import Transit
from PyQt4 import QtCore
from Logger import logger
import re

class TaskResult(QtCore.QObject):
    
    def __init__(self):
        super(TaskResult, self).__init__()
        self.phases = []
        self.values = []
        
class TaskEvent(QtCore.QObject):

     start      = QtCore.pyqtSignal()
     progress   = QtCore.pyqtSignal(int)
     result     = QtCore.pyqtSignal(object)
     stop       = QtCore.pyqtSignal()

class Task(QtCore.QObject):
    

    _tasks = [] 
    event = TaskEvent()
    
    def __init__(self):
        super(Task, self).__init__()
        self.input = TaskInput()
        self.result = TaskResult()
        self.completed = 0
        self.event = TaskEvent()
        pass
    
    def start(self):
        # keep Task.add here because thread is killed when no reference is stored somewhere
        Task.add(self)

        self.thread = Transit()
        self.thread.set_orbit_radius(self.input.semi_major_axis)
        self.thread.set_star_radius(self.input.star_radius)
        self.thread.set_planet_radius(self.input.planet_radius)
        self.thread.set_star_temperature(self.input.star_temperature)
        self.thread.set_planet_temperature(self.input.planet_temperature)
        self.thread.set_star_darkening(self.input.darkening)
        self.thread.set_phase_start(self.input.phase_start)
        self.thread.set_phase_end(self.input.phase_end)
        self.thread.set_phase_step(self.input.phase_step)
        
        
        self.thread.event.progress.connect(self._onProgress)
        self.thread.event.complete.connect(self._onComplete)
        self.thread.event.stop.connect(self._onStop)
        self.thread.start()
        self.event.start.emit()
        Task.event.start.emit()
        
    def _onProgress(self, progress):
        logger.info("Task.onProgress(" + str(progress) + ")")
        self.event.progress.emit(progress)
        Task.event.progress.emit(progress)
        
    def _onComplete(self, transitResult):
        logger.info("Task.onComplete")
        result = TaskResult()
        result.phases = transitResult.phases
        result.values = transitResult.values
        self.event.result.emit(result)
        Task.event.result.emit(result)
        
    def _onStop(self):
        logger.info("Task.onStop")
        self.event.stop.emit()
        Task.event.stop.emit()
        pass
        
    def stop(self):
        del Task._tasks[Task._tasks.__len__()-1]
        if self.thread :
            self.thread.stop()
    
    @staticmethod
    def last():
        return Task._tasks[Task._tasks.__len__()-1]
    
    @staticmethod
    def add(task):
        Task._tasks.append(task)
    
class TaskInput(object):
    
    def __init__(self):
        self.semi_major_axis = float(0.0)
        self.star_radius = float(0.0)
        self.planet_radius = float(0.0)
        self.star_temperature = float(0.0)
        self.planet_temperature = float(0.0)
        self.inclination = float(0.0)
        self.darkening = float(0.0)
        self.phase_start = float(0.0)
        self.phase_end = float(0.0)
        self.phase_step = float(0.0)
        pass
       
        
class TaskImportedResult(TaskResult):
   
   def __init__(self):
       super(TaskImportedResult, self).__init__()
        
        
class TaskImporter(QtCore.QObject):
    
    @staticmethod
    def loadFile(filename):
        imported = TaskImportedResult()
        print imported.phases
        with open(filename, 'rb') as csvfile:
            for line in csvfile.readlines():
                m = re.search('(-?\d+\.\d+)(\D+?)(-?\d+\.\d+)', line)
                
                if not m is None:
                    imported.phases.append(float(m.group(1)))
                    imported.values.append(float(m.group(3)))
                
        return imported
    
    @staticmethod
    def getFormats():
        return ['dat', 'csv']