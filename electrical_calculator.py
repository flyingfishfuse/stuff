import sys
from optparse import OptionParser
import sys, getopt
import math, cmath

yotta = 1000000000000000000000000#
zetta = 1000000000000000000000  #
exa =  1000000000000000000      #
peta = 1000000000000000        #
tera = 1000000000000         #
giga = 1000000000          #
mega = 1000000          #
kilo = 1000          #
hecto = 100       #
deca = 10       #
deci = 0.1     #
centi = 0.01      #
milli = 0.001       #
micro = 0.00001       #
nano = 0.00000001        #
pico = 0.000000000001      #
femto = 0.000000000000001    #
atto = 0.000000000000000001    #
zepto = 0.000000000000000000001 #
yocto = 0.000000000000000000000001

pi = 3.14159
Vbe= 0.7 # volts

#freq = 10000000
#N1 = [1,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128]
#HS_DIV = [11,9,7,6,5,4]
#upper = 5670000000/freq
#lower = 4850000000/freq



# THIS IS AN SI570 FREQUENCY SET CALCULATOR
#class Freq_Calc:
#    def _init_(self,freq):
#        N1 = [1,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128]
#        HS_DIV = [11,9,7,6,5,4]
#        upper = 5670000000/freq
#        lower = 4850000000/freq
#        freq = 10000000
#        for n1 in N1:
#            for hsdiv in HS_DIV:
#                actual = hsdiv * n1
#                if (upper > actual and lower < actual):
#                    print  "hsdiv value", hsdiv
#                    print  "n1 value   ", n1
#
class LC_circuit:
    def __init__(self, inductance, capacitance, voltage, current = 0,  series = 1, parallel = 0):
        '''
        LC circuit calculator.
            LC_circuit(inductance , capactitance, voltage, current = 0, series = 1, parallel = 0)

        REQUIRED parameters are inductance, capacitance, and voltage.
        '''
        self.inductance               = inductance
        self.capacitance              = capacitance
        self.voltage                  = voltage
        self.current                  = current
        self.resonant_frequency_hertz = 1/(2 * pi * math.sqrt(self.inductance * self.capacitance))
        self.resonant_frequency_w     = math.sqrt(1/(self.inductance * self.capacitance))
        if series:
            self.impedance            = ((math.pow(self.resonant_frequency_w , 2) * self.inductance * self.capacitance - 1)* 1j) / (self.resonant_frequency_w * self.capacitance)
        elif parallel:
            self.impedance            = (-1j * self.resonant_frequency_w * self.inductance)/ (math.pow(self.resonant_frequency_w , 2) * self.inductance * self.capacitance -1)
        else:
            print "AGGGGHHHHH MY LC_circuit IS BURNING AGHHHHHHH!!!"

class Transistor_NPN:
    def __init__ (gain , current_in, voltage_in,frequency, resistor1, resistor2, resistor3):
    '''
    Transistor_NPN(gain,current_in, voltage_in, frequency, res1, res2, res3))

    The resistors are as follows, r1 is collector, r2 is base, r3 is emitter

    REQUIRED parameters are current, voltage, resistors 1-3
    '''

        self.gain           = gain
        self.current_in     = current_in
        self.voltage_in     = voltage_in
        self.DCcurrentGain  = self.collectorcurrent / self.basecurrent
        self.emitteralpha   = self.collectorcurrent / self.emittercurrent
        self.resistor1      = Resistor(resistor1) # collector
        self.resistor2      = Resistor(resistor2) # base
        self.resistor3      = Resistor(resistor3) # emitter
        self.basecurrent    = (voltage_in - Vbe) / self.resistor2.resistance
        self.emittercurrent = (voltage_in - Vbe) / (self.resistor2.resistance/gain)





class RLC_circuit:
    def _init_(self, resistance, inductance, capacitance, voltage, current, frequency ):

        self.resistance               = resistance
        self.inductance               = inductance
        self.capacitance              = capacitance
        self.voltage                  = voltage
        self.current                  = current
        self.resonant_frequency_w = 2 * pi * frequency
        if series:
            self.attenuation = self.resistance / 2 * self.inductance
            self.resonant_frequency = 1/(math.sqrt(self.inductance * self.capacitance))
            self.damping_factor = (self.resistance/2) * (math.sqrt(self.capacitance * self.inductance))
            self.q_factor = 1/self.resistance * math.sqrt(self.inductance/self.capacitance)
            self.bandwidth = 2 * self.attenuation / self.resonant_frequency
            if self.damping_factor < 1:
                self.underdamped = 1
            elif self.damping_factor > 1:
                self.overdamped = 1
            else:
                print "you managed to make a number that is neither greater than or less than or even equal to 1 ... GOOD JOB!"
        elif parallel:
            self.attenuation = 1 / (2 * self.resistance * self.capacitance)
            self.damping_factor = (1/(2 * self.resistance))* math.sqrt(self.inductance / self.capacitance)
            self.q_factor = self.resistance * math.sqrt(self.capacitance/self.inductance)
            self.bandwidth = (1/ self.resistance) * math.sqrt(self.inductance/self.capacitance)
            self.frequency_domain = 1/(1j * self.resonant_frequency * self.inductance) + 1j * self.resonant_frequency * self.capacitance + 1/self.resistance
            if self.damping_factor < 1:
                self.underdamped = 1
            elif self.damping_factor > 1:
                self.overdamped = 1
            else:
                print "you managed to make a number that is neither greater than or less than or even equal to 1 ... GOOD JOB!"

class Resistor:
    def __init__ (self, resistance, current, voltage):
        self.resistance   = resistance
        self.voltage      = voltage
        self.current      = self.voltage / self.resistance
        self.resistance   = self.voltage / self.current
        self.voltage      = self.resistance * self.current
        self.loss         = self.voltage^2 / self.resistance


class Inductor:
    def __init__ (self, inductance, current, voltage, frequency = 0):
        self.inductance   = inductance
        self.current      = current
        self.voltage      = voltage
        self.frequency    = frequency
        self.stored_e     = 1/2 * (inductance * current^2)
        self.qfactor      = (2 * pi * self.frequency * self.inductance) / self.resistance


class Capacitor:
    def __init__(self, capacitance, voltage, frequency):
        self.capacitance    = capacitance
        self.voltage        = voltage
        self.frequency      = frequency
        self.charge_ratio   = self.capacitance * self.voltage
        self.efield_energy  = 1/2 * voltage * self.charge_ratio
        self.reactance      = -(1/(2 * pi * self.frequency * self.capacitance))
        self.impedance      = -(1j/(2 * pi * self.frequency * self.capacitance))



class RL_Circuit:
    def __init__(self, resistance , inductance , frequency, voltage_in, series = 1, parallel = 0 ):
        self.resistance        = resistance
        self.inductance        = inductance
        self.frequency         = frequency
        self.voltage_in        = voltage_in
        self.complex_frequency = 1j * (2 * pi * self.frequency)
        self.complex_impedance = self.inductance * self.complex_frequency


#    def _init_(self, number, unit):
#        self.unit = unit
#        self.number = number
#        if unit == "mega":
#            return self.number*self.mega
#        elif self.unit == "kilo":
#            return self.number*self.kilo
#        elif self.unit == "hecto":
#            return self.number*self.hecto
#        elif self.unit == "deca":
#            return self.number*self.deca
#        elif self.unit == "deci":
#            return self.number*self.deci
#        elif self.unit == "milli":
#            return self.number*self.milli
#        elif self.unit == "micro":
#            return self.number*self.micro
#        elif self.unit == "pico":
#            return self.number*self.pico
#        elif self.unit == "nano":
#            return self.number*self.nano
#        else:
#            print "converter function is not designed for bananas or units measuring bananas or bacon"
