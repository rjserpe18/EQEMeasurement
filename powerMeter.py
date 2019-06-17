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
        self.fullName = 'test'
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
            while (deviation > 2 or deviation < -2):
                return False
            return True

        def percentSTDV(dataSet):
            return 100 * statistics.stdev(dataSet) / statistics.mean(dataSet)

        data = []

        i = 1

        deviation = 900

        while (deviationIsSteady(deviation) == False):
            print("")
            print("trial " + str(i) + " at wavelength: " + str(self.getWavelength()))

            data = []

            print("measuring values")
            for j in range(1, 6, 1):
                data.append(self.getPower())
                time.sleep(1)

            deviation = percentSTDV(data)
            print("stdv for trial " + str(i) + ": " + str(deviation))

            print("data set for trial " + str(i) + ":" + str(data))

            if (deviation > -2 and deviation < 2) or (-7*10**-6 < statistics.mean(data) < 7*10**-6):
                print("data steady, mean= ", statistics.mean(data))
                return (statistics.mean(data))
            else:
                print("data unsteady. remeasuring....")

            i += 1



    def zero(self):
        reading = self.measurePowerUntilSteady()
        if reading < 0:
            shift = 0 - reading

        if reading > 0:
            shift = 0-reading
        return shift

    # self.powerMeter.write('sense:zero')

    def measure(self):
        time.sleep(30)
        shift = self.zero()

        input('turn laser on and press enter')
        print('waiting...')
        time.sleep(15)
        reading = self.measurePowerUntilSteady()
        result = (reading + shift)*10**6
        print('result= ',result,'µW')



