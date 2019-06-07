import visa
import time
import statistics

class PowerMeter:



    def __init__(self,address,nickName):

        rm = visa.ResourceManager()

        powerMeter = rm.open_resource(address)

        self.resourceManager = rm

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

    def measurePowerUntilSteady(self):

        def deviationIsSteady(deviation):
            while (deviation > 1):
                return False
            return True

        def percentSTDV(dataSet):
            return 100 * statistics.stdev(dataSet) / statistics.mean(dataSet)

        data = []

        i = 1

        deviation = 1.1

        while (deviationIsSteady(deviation) == False):

            print("")
            print("trial " + str(i) + " at wavelength: " + str(thorLabs.getWavelength()))

            data = []

            print("measuring values")
            for j in range(1, 6, 1):
                data.append(thorLabs.getPower())
                time.sleep(1)

            print("assessing data stability...")
            time.sleep(2)

            deviation = percentSTDV(data)
            print("stdv for trial " + str(i) + ": " + str(deviation))

            print("data set for trial " + str(i) + ":" + str(data))

            if (deviation > 1):
                print("data unsteady. remeasuring....")
            else:
                print("data steady!")

            i += 1

        print(str(statistics.mean(data))+(" W"))



thorLabs = PowerMeter('USB0::0x1313::0x8072::P2003101::0::INSTR', "thor labs")

thorLabs.setWavelength(638)

thorLabs.measurePowerUntilSteady()













