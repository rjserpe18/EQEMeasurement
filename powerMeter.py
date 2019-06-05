import visa
import Instrument

class PowerMeter:



    def __init__(self,address,nickName):
        rm = visa.ResourceManager()

        powerMeter = rm.open_resource(address)


        self.address = address
        self.fullName = powerMeter.query('*IDN?')
        self.nickName = nickName


    def getNickName(self):
        return "Nickname: "+self.nickName

    def getFullName(self):
        return "Full Name: "+self.fullName

    def getAddress(self):
        return "Address: "+self.address




tester = PowerMeter('USB0::0x1313::0x8072::P2003101::0::INSTR','tester')

print(tester.getNickName())
print(tester.getAddress())
print(tester.getFullName())

