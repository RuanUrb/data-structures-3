# ----------------------------------------------------
# ----------------------------------------------------
import sys
class IdxPrimario:

    # *** atributos
    __arquivoDados    = None   # string
    __arquivoIndices  = None   # string
    __arquivoIndicesSec = None
    __tabelaIndicesP   = list() # lista de tuplas ( RRN , CC )
    __tabelaIndicesS = list()

    #-------------------------------------------------------
    #-------------------------------------------------------

    def __init__(self, dataFile = None, inputFile = None, outputFile = None, debug = False):

        if(dataFile == None or inputFile == None or outputFile == None):
            raise Exception("Por favor, informe o diretório dos arquivos de dados e indices")
            exit(1)
        else:
            # abrindo arquivo de dados
            try:
                self.__arquivoDados = open(dataFile, "r+")
            except FileNotFoundError as error:
                print(error)
                exit(1)

            #abrindo arquivo de input
            self.__arquivoInput = open(inputFile, "r+")
            self.__arquivoOutput = open(outputFile, "w+")
            # imprimindo a lista de
            #print(self.__tabelaIndicesP)

            #criar a tabela de indices
            linhas = self.__arquivoDados.readlines()

            #  - percorrer o arquivo de dados
            # 0 até qtdeLinhas (len/size linhas) - header = linhas[0]
            size, top, qtd, status = self.readHeader(linhas[0])

            input = self.__arquivoInput.readlines()
            categoria = input[0]
            categoria = categoria.strip()
            consulta = input[1]
            consulta = consulta.strip()


            for index in range(1, len(linhas)):
                keyP = self.criaChaveCanonica(registro = linhas[index])
                keyS = self.criaChaveSecundaria(registro = linhas[index], categoria = categoria)
                RRN = index - 1
                tuplaP = (RRN, keyP)
                tuplaS = (keyS, keyP)
                self.__tabelaIndicesP.append(tuplaP)
                self.__tabelaIndicesS.append(tuplaS)

            # ordenar a tabela de indices
            self.__tabelaIndicesP.sort(key = lambda tup: tup[1])
            self.__tabelaIndicesS.sort(key = lambda tup: tup[0])
            found = False
            for i in self.__tabelaIndicesS:
                canonKey = self.pesquisarSecundario(consulta = consulta, i = i)
                print(f"canon key: {canonKey}")
                if(canonKey != -1):
                    found = True
                    registro = self.pesquisarPrimario(canonKey=canonKey, linhas = linhas, size = size) 
                    print(registro)
                    self.__arquivoOutput.write(registro)
            if(found != True):
                self.__arquivoOutput.write("Nenhum registro encontrado")  
            self.__del__()
            #print(canonKey)
    def getIdxPrim(self):
        return self.__tabelaIndicesP

    def getIdxSec(self):
        return self.__tabelaIndicesS

    def criaChaveSecundaria(self, registro, categoria):
        aux = registro.strip()
        tokens = aux.split("|")
        if(categoria == "ano"):
            keyS = tokens[0]
        elif(categoria == "duracao"):
            keyS = tokens[1]
        elif(categoria == "titulo"):
            keyS = tokens[2]
        elif(categoria == "artista"):
            keyS = tokens[3]    
        elif(categoria == "genero"):
            keyS = tokens[4] 
        elif(categoria == "idioma"):
            keyS = tokens[5]    
        else:
            self.__arquivoOutput.write("Categoria invalida")
            exit(1)     

        keyS = keyS.upper()
        return keyS

    def criaChaveCanonica(self, registro):
        aux = registro.strip()
        tokens = aux.split("|")
        key = tokens[4] + tokens[2]  # ano +  titulo
        key = key.upper()
        key = key.replace(" ", "")
        #print(key)
        return (key)

    def imprimeTabelaIndices(self, tabela):
        for element in tabela:
            print(element)

    #destrutor
    def __del__(self):    
        self.__arquivoDados.close()
        self.__arquivoInput.close()
        self.__arquivoOutput.close()

    def readHeader(self, header):
        # para ler todos os metadados do cabecalho corretamente
        sizeSplit = header.split(" ")
        size = sizeSplit[0].split("SIZE=")
        

        topSplit = header.split(" ")
        top = topSplit[1].split("TOP=")

        registerSplit = header.split(" ")
        registerQtd = registerSplit[2].split("QTDE=")  
        
        statusSplit = header.split(" ")
        status = statusSplit[3].split("STATUS=")

        
        return size[1], top[1], registerQtd[1], status[1]

    def pesquisarSecundario(self, consulta, i):
        print(f"{i[0]} + {consulta}")
        if(consulta.upper() in i[0]):
            print(i[0])
            return i[1]
        return -1

    def pesquisarPrimario(self, canonKey, linhas, size):
        for i in self.getIdxPrim():
            #print(self.getIdxPrim())
            #print(i[0])
            if i[1] == canonKey:
                return linhas[int(i[0]) + 1]
        

def main():
    if(len(sys.argv)!=4):
        print("Número incorreto de parâmetros. \nSaindo do programa...")
        exit(1)
    obj = IdxPrimario(dataFile = sys.argv[1],
     inputFile = sys.argv[2], outputFile= sys.argv[3])
    
    


if(__name__ == '__main__'):
        main()
