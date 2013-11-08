import Individual
import random
import math

'-----CONTROL PARAMETERS--------'
CHROM_LENGTH=16
POPULATION_SIZE=20
PMUT=0.05
MAX_GEN=100
GEN_REP=20
ELITE=1
MAXMIN=-1
beststring=Individual.Individual(CHROM_LENGTH)
verybest=Individual.Individual(CHROM_LENGTH)
population=[]
selected=[]
'-------------------------------'

def init_indiv():
    i=Individual.Individual(16)
    return i

def init_pop():
    'create new population with random chromosome values'
    'also assign fitness and value based on bitstring'
    for i in range (0, POPULATION_SIZE):
        x=init_indiv()
        x.setValue(decode(x))
        x.setFitness(evaluate(x))
        population.insert(i,x)
    return population

def getPreviousBest(population):
    for i in population:
        if MAXMIN*i.getFitness() > MAXMIN * beststring.getFitness():
            'overwrite local best beststring with i'
            beststring.setValue(i.getValue())
            beststring.overwriteChrome(i.getChromosome())
            beststring.setFitness(i.getFitness())
        if MAXMIN*beststring.getFitness() > MAXMIN*verybest.getFitness():
            'overwrite global best with local best'
            verybest.setValue(beststring.getValue())
            verybest.overwriteChrome(beststring.getChromosome())
            verybest.setFitness(beststring.getFitness())
    return

def decode(indiv):
    value=0
    for i in range(0, CHROM_LENGTH):
        value+= ( math.pow(2, i) ) * ( indiv.getIndivChrome(CHROM_LENGTH-1-i) );
    return value

def evaluate(indiv):
    value=indiv.getValue()
    convDec=convRange(value)
    ans=( 0.1*math.fabs(convDec) - math.sin(convDec) )
    return ans

def convRange(raw):
    return ( (raw/65535.0) * 120)- 60

def coinFlip(prob):
    i=random.random()
    if i < prob:
        return 0
    else:
        return 1

'3-2 tournament selection'
def selection(population):
    del selected[0:len(selected)]
    for i in range (0, POPULATION_SIZE):
        'skip even indices to ensure only 30 individuals are selected for new population'
        if i % 2 == 0:
            continue
        'generate 3 random indices'
        r=random.random()*POPULATION_SIZE;
        s=random.random()*POPULATION_SIZE;
        t=random.random()*POPULATION_SIZE;

        ri=population[int(r)];
        si=population[int(s)];
        ti=population[int(t)];

        rf=ri.getFitness()
        sf=si.getFitness()
        tf=ti.getFitness()

        if rf >= sf and rf >= tf:
            if sf > tf:
                selected.insert(i, ri)
                selected.insert(i, si)
            else:
                selected.insert(i, ri)
                selected.insert(i, ti)
        elif sf >= rf and sf >= tf:
            if rf > tf:
                selected.insert(i, si)
                selected.insert(i, ri)
            else:
                selected.insert(i, si)
                selected.insert(i, ti)
        elif tf >= rf and tf >= sf:
                if rf > sf:
                    selected.insert(i, ti)
                    selected.insert(i, ri)
                else:
                    selected.insert(i, ti)
                    selected.insert(i, si)
        
    return selected

def mutation(population):
    for i in population:
        for j in range (0, len(i.getChromosome())):
            if coinFlip(PMUT)==0:
                if i.getIndivChrome(j)==1:
                    i.setChromosome(1, j)
                else:
                    i.setChromosome(0, j)

def crossover (parent1, parent2, population):
    child1=Individual.Individual(CHROM_LENGTH)
    child2=Individual.Individual(CHROM_LENGTH)
    site = int(random.random()*CHROM_LENGTH)
    for i in range(0, CHROM_LENGTH):
        parent1Chrome=parent1.getIndivChrome(i)
        parent2Chrome=parent2.getIndivChrome(i)
        if i <= site or site==0:
            child1.setChromosome(parent1Chrome,i)
            child2.setChromosome(parent2Chrome,i)
        else:
            child1.setChromosome(parent2Chrome,i)
            child2.setChromosome(parent1Chrome,i)

    'replace parents with children'
    parent1.overwriteChrome(child1.getChromosome())
    parent2.overwriteChrome(child2.getChromosome())
    
def elite(population):
    if MAXMIN*beststring.getFitness() > MAXMIN*evaluate(population[0]):
        population[0].setFitness(beststring.getFitness())
        population[0].setValue(beststring.getValue())
        population[0].overwriteChrome(beststring.getChromosome())

def statistics(population, selected, curGen):
    print "\n\nGeneration: "+str(curGen)+"\nSelected Strings: "
    for s in selected:
        s.printChromosome()
    print "\n         x          f(x)            new_str               X"
    for i in population:
        out=""
        for j in range (0, CHROM_LENGTH):
            out+=str( i.getIndivChrome(j) )
        print str( convRange(i.getValue()) )+"\t"+str( i.getFitness() )+"\t"+out+"\t"+str( convRange(decode(i)) )
    print "\n\nBest string\n------------"
    out=""
    for j in range (0, CHROM_LENGTH):
        out+=str( beststring.getIndivChrome(j) )
    print out
    print "\nValue: " + str( convRange(beststring.getValue()) )
    print "Fitness: " + str( beststring.getFitness() )

def finalReport(population):
    print "======================================================="
    print "Best result of all generations:"
    best=verybest.getChromosome()
    out=""
    for i in best:
        out+=str(i)
    print out
    print "Decoded value " + str( convRange(verybest.getValue()) )
    print "Fitness " + str( verybest.getFitness() )
                          	
def main():
    'clear previous population list if running more than once'
    del population[0:len(population)]
    
    curGen=0
    
    if MAXMIN==-1:
        verybest.setFitness(999999)
    else:
        verybest.setFitness(-999999)
        
    init_pop()
    curGen=0
    
    'main loop'
    while (curGen < MAX_GEN):
        getPreviousBest(population)
        
        selected=selection(population)
        
        for i in range (0, POPULATION_SIZE-1):
            if i % 2 == 0:
                continue
            elif i == POPULATION_SIZE:
                break
            crossover(selected[i], selected[i+1], population)
        
        mutation(population)
        
        for i in population:
            i.setValue(decode(i))
            i.setFitness(evaluate(i))

        if ELITE==1:
            elite(population)

        if curGen%GEN_REP==0:
            statistics(population, selected, curGen)

        curGen+=1

    finalReport(population)

if __name__ == '__main__':
    main()
        
    
    
        
    
    

    

