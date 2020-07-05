import random
import numpy as np
from numpy.random import choice
import pandas as pd  
import requests
url='https://lf8q0kx152.execute-api.us-east-2.amazonaws.com/default/computeFitnessScore'
  

size=8

def noSafe_pos(a,b):
    #global diagSet 
    global df
    diagSet=set()
    for i in range(0,size):
        diagSet.add((a,i))
        diagSet.add((i,b))
    for i in range(0,size):
        for j in range(0,size):
            if (a-b)==(i-j):
                diagSet.add((i,j))
            if (a+b)==(i+j):
                diagSet.add((i,j))
    return diagSet
   
def getScore(c):
    j=0
    l=0
    checkSet=set()
    for i in c:
        checkSet.add((int(i),int(j)))
        j+=1
    for i in checkSet:
        checkSetexcept=checkSet.copy()
        checkSetexcept.remove(i)
        for k in checkSetexcept:
            if k in noSafe_pos(i[0],i[1]) :
                l-=1
    return l
                

totalPopulation = 150
row_list = [x for x in range(0,size)] 
populationData = []
fitnessData = []
secure_random = random.SystemRandom()
for outloop in range(totalPopulation):
    randomData = []
    fitnessScore = 0
    #selectedData=""
    secure_random.shuffle(row_list)
    selectedData=row_list.copy()
    populationData.append(selectedData)
    fitnessData.append(getScore(selectedData))
probabilityDist = []
for outloop in range(totalPopulation):
  probabilityDist.append(fitnessData[outloop]/size)
probDataFrame = pd.DataFrame({'String':populationData,'FitnessScore':fitnessData,'Probability':probabilityDist})
probDataFrame = probDataFrame.sort_values(['Probability'],ascending=False)
probDataFrame = probDataFrame.reset_index(drop=True)
print(probDataFrame)
generationCount = 10000
child1=[]
child2=[]
for loop in range(generationCount):
  draw=[]
  draw.append(probDataFrame[0:1]["String"].values[0])
  draw.append(probDataFrame[1:2]["String"].values[0])
  if probDataFrame['FitnessScore'][0] == 0:
    print(probDataFrame['String'][0])
    finalResult=probDataFrame['String'][0]
    break
  secure_random.shuffle(row_list)
  child1 = row_list.copy()
  secure_random.shuffle(row_list)
  child2 = row_list.copy()
  populationData.append(child1)
  populationData.append(child2)
  totalPopulation = len(populationData)
  fitnessData.append(getScore(child1))
  fitnessData.append(getScore(child2))
  probabilityDist.append(getScore(child1)/size)
  probabilityDist.append(getScore(child1)/size)
  probDataFrame = pd.DataFrame({'String':populationData,'FitnessScore':fitnessData,'Probability':probabilityDist})
  probDataFrame = probDataFrame.sort_values(['Probability'],ascending=False)
  probDataFrame = probDataFrame.reset_index(drop=True)
  print('Generation ',str(loop),' ',' Average Fitness Score ',str(probDataFrame["FitnessScore"].mean()),' ', ''.join(str(child1)),' ',str(getScore(child1)),''.join(str(child2)),str(getScore(child2)))

x=requests.post(url,json={"qconfig":"finalResult","userID":"689144","githubLink":"https://github.com/naveen-jaladi/Final_nQueen/blob/master/nQueen.py"}) 
print(x.text)