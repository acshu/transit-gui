# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtSignal, QThread
from transitlib.transit import Transit as TransitLib

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
        