import random
import math
import matplotlib.pyplot as plt

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

       



def ACO(matrix, size, maxIter):
    colonySize = 100
    attractiveness = [[0 if i == j else 1/(matrix[i][j] + 0.00001) for j in range(size)] for i in range(size)]      
    initEvap = 0.0001
    pheremone = [[initEvap for i in range(size)] for i in range(size)]
    alpha = 2
    beta = 15
    Q = 10
    evaporation = 0.1
    iteration = 0
    dupeRemoval = 0.5
    def pickNext(current, allowed):
        denominator = 0
        for node in allowed:
            denominator += (pheremone[current][node] ** alpha)*(attractiveness[current][node]**beta)
        probabilities = [0 for i in range(size)]

        for i in allowed:
            

            probabilities[i] =((pheremone[current][i] ** alpha)*(attractiveness[current][i]**beta))/denominator

        rand = random.random()

        
        for i in range(size):
            rand -= probabilities[i]
            if rand <= 0:
                return i
    def removeBias(tours,tourLength):
        newTours = []
        newLengths=[]
        seen= set()
        
        for i in range(len(tourLength)):
            if tourLength[i] not in seen:
                
                newLengths.append(tourLength[i])
                newTours.append(tours[i])
                seen.add(tourLength[i])
            else:
                if random.random() < dupeRemoval:
                    newLengths.append(tourLength[i])
                    newTours.append(tours[i])
                    
        return newTours,newLengths
    def createSolutions():
        tours = []
        tourLength = []
        for i in range(colonySize):
            allowed = [i for i in range(1,size)]
            startNode = random.randint(0,size-1)
            tour = [startNode]
            length = 0
            current = startNode
            while len(allowed) > 0:
                temp = current
                current = pickNext(current,allowed)
                tour.append(current)
                allowed.remove(current)
                length += matrix[temp][current]
            length += matrix[current][startNode]
            tours.append(tour)
            tourLength.append(length)
        return tours, tourLength

    def pheremoneUpdate(tours,tourLength):

        for i in range(size):
            
            pheremone[i] = [x*(1-evaporation) if x > initEvap else initEvap for x in pheremone[i]]
            
        for i in range(len(tours)):
            deltaT = Q/tourLength[i]
            for j in range(size):
                pheremone[tours[i][j]][tours[i][(j+1)%(size-1)]] += deltaT
##    def pheremoneUpdate(bestTour,bestLength):
##        for i in range(size):
##            pheremone[i] = [x*(1-evaporation) if x > initEvap else initEvap for x in pheremone[i]]
##            deltaT = Q/bestLength
##            pheremone[bestTour[i]][bestTour[(i+1)%(size-1)]] += deltaT         

    
    while iteration < maxIter:
        tours, tourLength = createSolutions()
        
        tours, tourLength = removeBias(tours,tourLength)
        
        pheremoneUpdate(tours,tourLength)
        bestLength = min(tourLength)                            
        bestTour = tours[tourLength.index(bestLength)]
        #pheremoneUpdate(bestTour,bestLength)
        if iteration%1==0:
            print(bestLength)
        iteration += 1
       
    return bestLength,bestTour
        
filename = "AISearchfile017"
data = readFile("NEW"+filename+".txt")
matrix = dataToArray(data)
for i in range(10):
    print(i)
    length,tour = ACO(matrix,data[1],10)
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
    
    




    




##plt.style.use("seaborn-whitegrid")
##fig = plt.figure()
##ax = plt.axes()
##plt.plot(listOfTours)
##plt.show()








        
    
