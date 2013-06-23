import random

class Individual:
    'class for Individual bitstrings'
    def __init__(self, chromLength):
        self.value=0
        self.fitness=0
        self.chromosome=[]
        for i in range (0, chromLength):
            self.chromosome.insert( i,random.randrange(0,2) )

    def getValue(self):
        return self.value
    def getFitness(self):
        return self.fitness
    def getChromosome(self):
        return self.chromosome
    def toString(self):
        return str(self.chromosome)
    def getIndivChrome(self, index):
        return self.chromosome[index]
    def overwriteChrome(self, newChrome):
        for i in range ( 0, len(newChrome) ):
            self.chromosome[i]=newChrome[i]
    def printChromosome(self):
        out=""
        for i in range ( 0, len(self.chromosome) ):
            out+=str( self.getIndivChrome(i) )
        print out
    def setValue(self, newValue):
        self.value=newValue
    def setFitness(self, newValue):
        self.fitness=newValue
    def setChromosome(self, val, position):
        self.chromosome[position]=val
        
    
    
