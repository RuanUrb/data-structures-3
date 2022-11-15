import numpy as np
import sys

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
    inputFile = open(sys.argv[1], 'r')
    outputFile = open(sys.argv[2], "w+")
    tempfile = open(sys.argv[3], "w+")
    return inputFile, outputFile, tempfile

def readFile(arquivo):
    return arquivo.readlines()

def readHeader(header):
    # para ler todos os metadados do cabecalho corretamente
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

######################## SORTS ########################################
def insertionSort(array, rrnList):   
    for step in range(1, len(array)):
        key = array[step]
        key2 = rrnList[step]
        j = step - 1       
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            rrnList[j + 1] = rrnList[j]
            j = j - 1
        array[j + 1] = key
        rrnList[j + 1] = key2
    
def mergeSort(array, rrnList):

    if len(array) > 1:
        r = len(array)//2
        L = array[:r]
        M = array[r:]
        L2 = rrnList[:r]
        M2 = rrnList[r:]
        mergeSort(L, L2)
        mergeSort(M, M2)

        i = j = k = 0
        while i < len(L) and j < len(M):
            
            if L[i] < M[j]:
                array[k] = L[i]
                rrnList[k] = L2[i]
                i += 1
            else:
                array[k] = M[j]
                rrnList[k] = M2[j]
                j += 1
            k += 1

        while i < len(L):
            array[k] = L[i]
            rrnList[k] = L2[i]
            i += 1
            k += 1
            
        while j < len(M):
            array[k] = M[j]
            rrnList[k] = M2[j]
            j += 1
            k += 1   

def partition(array, rrnList, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
            (rrnList[i], rrnList[j]) = (rrnList[j], rrnList[i])
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    (rrnList[i + 1], rrnList[high]) = (rrnList[high], rrnList[i + 1])

    return i + 1

def quickSort(array, rrnList, low, high):
    if low < high:
        pi = partition(array, rrnList, low, high)
        quickSort(array, rrnList, low, pi - 1)
        quickSort(array, rrnList, pi + 1, high)

def heapify(arr, rrnList, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[i] < arr[l]:
        largest = l
    if r < n and arr[largest] < arr[r]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        rrnList[i], rrnList[largest] = rrnList[largest], rrnList[i]
        heapify(arr, rrnList, n, largest)

def heapSort(arr, rrnList):
    n = len(arr)
    for i in range(n//2, -1, -1):
        heapify(arr, rrnList, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        rrnList[i], rrnList[0] = rrnList[0], rrnList[i]
        heapify(arr, rrnList, i, 0)
#######################################################################


def sortingRegisters(tempfile, keyList, rrnList, sort):
    low = 0
    high = len(keyList) - 1

    if(sort == 'Q'):
        quickSort(keyList, rrnList, low, high)
    elif(sort == 'I'):
        insertionSort(keyList, rrnList)
    elif(sort == 'H'):
        heapSort(keyList, rrnList)
    elif(sort == 'M'):
        mergeSort(keyList, rrnList)
    else:
        print("Invalid sort instruction.Exiting program...\n")
    return rrnList

def storeOrganizedData(rrnListSorted, outputFile, tempFile, size, registerQtd, header, order):
    tempFile.seek(0)
    test = tempFile.readline()
    
    order = order.strip()

    if(order == 'C'):
        outputFile.write(header)
        for i in range(0, int(registerQtd)):
            tempFile.seek(rrnListSorted[i] * (int(size)+2))
            linha = tempFile.readline()
            outputFile.write(f"{linha}")
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
    rrnListSorted = sortingRegisters(tempFile, keyList, rrnList, sort, order)
    storeOrganizedData(rrnListSorted, outputFile, tempFile, size, registerQtd, header, order)


if __name__ == '__main__':
    main()
