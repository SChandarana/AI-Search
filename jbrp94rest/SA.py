import random
import math
        

def readFile(fName):
    data = open(fName,'r')
    textFile = data.read();
    data.close()
    text = ""
    for i in textFile:
        if i == "," or i.isnumeric():
            text += i   
    out = [int(i) for i in text.split(",")[1:]]
    return  out[1:], out[0]

   
def createEmpty(size):
    empty = [[0 for i in range(size)]for z in range (size)]
    return empty

def dataToArray(data):
    size = data[1]
    distances = data[0]
    array = createEmpty(size)
    count = 0
    for i in range(size):
        for j in range(i,size):
            if i != j:
                value = distances[count]
                array[i][j] = value
                array[j][i] = value
                count += 1
                
    return array
        
def greedyTour(size,matrix):
    tour =[0]
    def pickLowest(node,remaining):
        lowestWeight = 0
        
        for x in remaining:
            if lowestWeight == 0 or matrix[node][x] < lowestWeight:
                lowestWeight = matrix[node][x]
                bestNode = x
        return bestNode
    node = 0
    while len(remaining) > 0:
        node = pickLowest(node,remaining)
        tour.append(node)
        remaining.remove(node)
    return tour

def createNeighbour(tour):
    x = 0
    y = 0
    copy = tour[:]
    while x >= y :

        x = random.randint(0,len(copy)-1)    
        y = random.randint(0,len(copy)-1)
    
        
    copy[x:y+1] = reversed(copy[x:y+1])
    return copy , x , y 

def weight(tour,matrix):
    length = 0
    for i in range(len(tour)):
        x = tour[i]
        y = tour[(i+1)%(len(tour))]
        length += matrix[x][y]
    return length

    
def annealing(matrix,size):
    initTemp = 50
    temp = initTemp
    tempChange = 0.999
    alpha = 0.000000001
    strategy = "dynamic"
    maxIter = 1000000
    initial = greedyTour(size,matrix)
    ##initial = [i for i in range(size)]
    ##random.shuffle(initial)
    best = initial
    bestWeight = weight(best, matrix)
    neighbourWeight = 0
    i = 0
    noBetter = 0
    def coolingFunction(temp,noBetter,strategy,i):
        if strategy == "dynamic":
            
            return temp*tempChange*(1+alpha)**noBetter
        if strategy == "exponential":
            return temp*(tempChange)
        if strategy == "linear":
            return initTemp/(1+alpha*i)
        if strategy == "quadratic":
            return initTemp/(1+alpha*i**2)
        
    while(i < maxIter and temp > 0):
        tour,x,y = createNeighbour(best)
        
        neighbourWeight = bestWeight
        neighbourWeight += matrix[tour[x]][tour[x-1]]
        neighbourWeight += matrix[tour[y]][tour[(y+1)%len(tour)]]
        neighbourWeight -= matrix[tour[x]][tour[(y+1)%len(tour)]]
        neighbourWeight -= matrix[tour[y]][tour[x-1]]
        
        e = bestWeight - neighbourWeight
        
        if e >= 0:
            best = tour
            bestWeight = neighbourWeight
            
        else:
            noBetter += 1
            if random.random() < math.exp(e/temp):
                best = tour
                bestWeight = neighbourWeight
                noBetter = 0
                
        temp  = coolingFunction(temp,noBetter,strategy,i)
        i+= 1
        if i%100000 == 0:
            print(bestWeight)
    return bestWeight,best

filename = "AISearchfile535"
data = readFile("NEW"+filename+".txt")
matrix = dataToArray(data)
for i in range(10):
    print(i)
    length,tour = annealing(matrix,data[1])
    bestLength = length
    with open("tourNEW"+filename+".txt","a+") as f:
        f.seek(0)
        for line in f.readlines():
            
            if "LENGTH" in line:
                
                bestLength = ''.join(x for x in line if x.isdigit())
                
        
        if length <= int(bestLength):
            f.seek(0)
            f.truncate()
            f.write("NAME = "+filename+",\n"+"TOURSIZE = "+str(data[1])+",\n")
            f.write("LENGTH = "+str(length)+",\n"+str(tour).replace(" ","").replace("[","").replace("]",""))
    
    
