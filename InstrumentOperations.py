def getWorkableAddress(grossAddress):

   return grossAddress[grossAddress.find("(")+3:grossAddress.find(")")-2]

oldAddress = "(u'USB0::0x1313::0x8072::P2003101::0::INSTR',)"

print(getWorkableAddress(oldAddress))

