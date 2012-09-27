# -*- coding: utf-8 -*-

import scipy
import scipy.integrate
import scipy.constants
import math
from PyQt4 import QtCore
import time

class TransitResult(QtCore.QObject):
    
    def __init__(self, phases=[], values=[]):
        super(TransitResult, self).__init__()
        self.phases = phases
        self.values = values
        
class TransitEvent(QtCore.QObject):
    
    progress = QtCore.pyqtSignal(int)
    complete = QtCore.pyqtSignal(object)
    stop     = QtCore.pyqtSignal()

class Transit(QtCore.QThread):

    event = TransitEvent()
    
    orbit_radius        = float(10)
    star_radius         = float(1)
    planet_radius       = float(0.1)
    star_temperature    = float(8000)
    planet_temperature  = float(2000)
    star_darkening      = float(0.5)
    
    phi_start       = float(0)
    phi_end         = float(1)
    phi_iterations  = float(50000)
    phi             = float(phi_start)
    completed       = 0

    phase1 = float(0)
    phase2 = float(0)
    phase6 = float(0)
    stopped = False
    
    def __init__(self):
        super(Transit, self).__init__()
        self.event = TransitEvent()
        self.phase1 = (1/(2*scipy.pi)) * scipy.arcsin((self.star_radius+self.planet_radius)/self.orbit_radius)
        self.phase2 = (1/(2*scipy.pi)) * scipy.arcsin((self.star_radius-self.planet_radius)/self.orbit_radius)
        self.phase6 = (1/(2*scipy.pi)) * scipy.arcsin(self.planet_radius/self.orbit_radius)
        return

    def stop(self):
        self.stopped = True
    
    def star_intensity(self):
        return scipy.constants.sigma * self.star_temperature**4
        
    def planet_intensity(self):
        return scipy.constants.sigma * self.planet_temperature**4
        
    def star_luminosity(self):
        return scipy.pi * self.star_radius**2 * self.star_intensity() * ( 1 - (self.star_darkening/3))
        
    def planet_luminosity(self):
        return scipy.pi * self.planet_radius**2 * self.planet_intensity()
        
    def x0(self):
        return self.orbit_radius * scipy.sin(2 * scipy.pi * self.phi)
        
    def x1(self, x):
        x0 = self.x0()

        if x0 == 0 :
            return 0
        
        return (x0**2 + x**2 - self.planet_radius**2)/(2*x0)
        
    def gamma(self, x):
        return scipy.arccos(self.x1(x)/x)
        
    def eq1(self, x):
        return self.star_intensity() * 2 * x * self.gamma(x) * ( 1 - self.star_darkening + self.star_darkening * scipy.sqrt((1-(x/self.star_radius)**2)))
        
    def eq2(self, x):
        return self.star_intensity() * 2 * scipy.pi * x * ( 1 - self.star_darkening + self.star_darkening * scipy.sqrt((1-(x/self.star_radius)**2)))
        
        
    def run(self):
        start = time.time()
        self.phi = self.phi_start
        phi_step = (self.phi_end - self.phi_start)/self.phi_iterations

        result = []
        phases = []
        
        iteration = 0
        maxPhase = max(self.phase1, self.phase2, self.phase6)
        while( self.phi <= self.phi_end and self.phi <= maxPhase ):
            
            if self.stopped:
                self.event.stop.emit()
                Transit.event.stop.emit()
                return
                
            current_result = None
            if self.phi >= min(self.phase1, self.phase2) and self.phi <= max(self.phase1, self.phase2) :
                a = self.x0() - self.planet_radius
                b = self.star_radius
                current_result = scipy.integrate.quad(self.eq1, a, b)
                current_result = current_result[0]
            elif self.phi >= min(self.phase2, self.phase6) and self.phi <= max(self.phase2, self.phase6):
                a = self.x0() - self.planet_radius
                b = self.x0() + self.planet_radius
                current_result = scipy.integrate.quad(self.eq1, a, b)
                current_result = current_result[0]
            elif self.phi <= self.phase6:
                a1 = 0
                b1 = self.planet_radius - self.x0() 
                a2 = self.planet_radius - self.x0()
                b2 = self.x0() + self.planet_radius
                
                result1 = scipy.integrate.quad(self.eq2, a1, b1)
                result2 = scipy.integrate.quad(self.eq1, a2, b2)
                current_result =  result1[0] + result2[0]
            else:
                current_result = None
                
                            
            if current_result is not None :
                phases.append(self.phi)
                result.append( 1 - ( -2.5*scipy.log10(((self.star_luminosity()+self.planet_luminosity())-current_result)/(self.star_luminosity()+self.planet_luminosity()))) )
            

            
            newcompleted = int((self.phi/maxPhase)*100)
            
            if newcompleted != self.completed :
                self.completed = newcompleted
                self.event.progress.emit(self.completed)
                Transit.event.progress.emit(self.completed)
            
            self.phi += phi_step
            iteration += 1
            
        
        transit_result = TransitResult(phases, result)
        self.event.complete.emit(transit_result)
        Transit.event.complete.emit(transit_result)
        print "Time: " + str(time.time() - start)