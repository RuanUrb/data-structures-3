import numpy as np

class Heroes:
    def __init__(self, key = None, fname = None, lname = None, hname = None, power = None, weakness = None, city = None, profession = None):
        self.key = key
        self.fname = fname
        self.lname = lname
        self.hname = hname
        self.power = power
        self.weakness = weakness
        self.city = city
        self.profession = profession
    
    def getKey(self):
        return self.key

    def getFname(self):
        return self.fname

    def getLname(self):
        return self.lname

    def getPower(self):
        return self.power

    def getHname(self):
        return self.hname

    def getWeakness(self):
        return self.weakness

    def getCity(self):
        return self.city

    def getProfession(self):
        return self.profession

def openFile():
    inputFile = open(r"C:\Users\zania\OneDrive\Documentos\PYTHON\ED2\Arquivos\Atividade3\input\input6.txt")
    outputFile = open("saida.txt", "w+")
    tempfile = open("temp.txt", "w+")
    return inputFile, outputFile, tempfile

def readFile(arquivo):
    data = arquivo.readlines()
    return data

def readHeader(header):
    sizeSplit = header.split(" ")
    size = sizeSplit[0].split("SIZE=")
    

    topSplit = header.split(" ")
    top = topSplit[1].split("TOP=")

    registerSplit = header.split(" ")
    registerQtd = registerSplit[2].split("QTDE=")  
     
    sortSplit = header.split(" ")
    sort = sortSplit[3].split("SORT=")

    orderSplit = header.split(" ")
    order = orderSplit[4].split("ORDER=")
    
    return size[1], top[1], registerQtd[1], sort[1], order[1] 

def sortFile():
    pass

def readData(inputDataVector, heroes, tempfile, size):
    keyList = []
    rrnList = []
    rrn = 0
    for lines in inputDataVector:
        data = lines.split("|")
        heroes = Heroes(key = data[0], fname = data[1], lname = data[2], hname = data[3], power = data[4], weakness = data[5], city = data[6], profession = data[7])
        keyList.append(data[0])
        rrnList.append(rrn)
        
        #tira o \n da profissao que atrapalha a formatação
        professionFormat = heroes.getProfession().strip()
        string = f"{heroes.getKey()}|{heroes.getFname()}|{heroes.getLname()}|{heroes.getHname()}|{heroes.getPower()}|{heroes.getWeakness()}|{heroes.getCity()}|{professionFormat}|"  
        tempfile.write(f"{string:{size}}\n")
        rrn += 1
    return keyList, rrnList

def sortingRegisters(tempfile, keyList, rrnList, sort, order):
    #array = np.array(zip(keyList, rrnList))
    #print(array)
    pairs = list(zip(keyList, rrnList))
    #print(pairs)
    array = np.array(pairs)
    #print(array)
    sorted = np.sort(array)
    print(sorted)
    #keyList, rrnList = zip(*sorted)
    #print(keyList, rrnList)

def sortingRegistersBeta(tempfile, keyList, rrnList, sort, order):
    sorting = sorted(zip(keyList, rrnList))
    keyList, rrnList = zip(*sorting)
    return list(rrnList)        

def storeOrganizedData(rrnListSorted, outputFile, tempFile, size, registerQtd, header, order):
    tempFile.seek(0)
    test = tempFile.readline()
    
    order = order.strip()

    if(order == 'C'):
        outputFile.write(header)
        for i in range(0, int(registerQtd)):
            tempFile.seek(rrnListSorted[i] * (int(size)+2))
            linha = tempFile.readline()
            outputFile.write(linha)
    elif(order == 'D'):
        outputFile.write(header)
        rrnListSorted.reverse()
        for i in range(0, int(registerQtd)):
            tempFile.seek(rrnListSorted[i] * (int(size)+2))
            linha = tempFile.readline()
            outputFile.write(linha)
    else:
        outputFile.write("Erro no arquivo")        

def main():
    inputFile, outputFile, tempFile = openFile()
    header = inputFile.readline()

    size, top, registerQtd, sort, order = readHeader(header)
    inputDataVector = readFile(inputFile)

    heroes = Heroes()
    keyList, rrnList = readData(inputDataVector, heroes, tempFile, size)

    #sortingRegisters(tempfile, keyList, rrnList, sort, order)
    rrnListSorted = sortingRegistersBeta(tempFile, keyList, rrnList, sort, order)

    storeOrganizedData(rrnListSorted, outputFile, tempFile, size, registerQtd, header, order)


if __name__ == '__main__':
    main()
