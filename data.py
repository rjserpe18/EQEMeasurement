f_open = open('values2.txt','r')

data = []

counter = 0

for line in f_open:

    if (counter%2 == 0):
         print(line[0:line.find("n")-1])

    counter+=1

