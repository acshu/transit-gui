# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from transitlib.transit import Transit as TransitLib

class TransitResult(QtCore.QObject):
    
    def __init__(self, phases=[], values=[]):
        super(TransitResult, self).__init__()
        self.phases = phases
        self.values = values
        
class TransitEvent(QtCore.QObject):
    
    progress = QtCore.pyqtSignal(int)
    complete = QtCore.pyqtSignal(object)
    stop     = QtCore.pyqtSignal()
    
class Transit(TransitLib, QtCore.QThread):

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
        result = TransitResult(phases, values)
        self.event.complete.emit(result)
        Transit.event.complete.emit(result)
        pass
        