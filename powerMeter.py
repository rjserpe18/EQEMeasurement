import visa
import time


class PowerMeter:



    def __init__(self,address,nickName):

        powerMeter = rm.open_resource(address)

        self.resourceManager = visa.ResourceManager()

        self.powerMeter = powerMeter

        self.address = address
        self.fullName = powerMeter.query('*IDN?')
        self.nickName = nickName




    def getNickName(self):
        return "Nickname: "+self.nickName

    def getFullName(self):
        return "Full Name: "+self.fullName

    def getAddress(self):
        return "Address: "+self.address

    def setWavelength(self, wavelength):

        if ( wavelength < 300 or wavelength > 1100):
            return 'invalid wavelength range'
        else:
            self.powerMeter.write('sense:corr:wav '+str(wavelength))
            return 'wavelength set to '+ str(wavelength)

    def getWavelength(self):
        return float(self.powerMeter.query('sense:corr:wav?'))


    def getPower(self):
        power_W = float(self.powerMeter.query('measure:power?'))
        return power_W





#this is the code we used to get those data points

# rm = visa.ResourceManager()
#
# thorLabs = PowerMeter('USB0::0x1313::0x8072::P2003101::0::INSTR', "thor labs")
#
# timeVals = []
# powerVals =[]
#
#
# thorLabs.setWavelength(638)
#
#
# for i in range (0,3600,30):
#     timeVals.append(i)
#     powerVals.append(thorLabs.getPower())
#     print(thorLabs.getPower())
#     print(i/60)
#
#     time.sleep(30)
