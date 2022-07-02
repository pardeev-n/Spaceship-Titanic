# -*- coding: utf-8 -*-
"""Test6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cJ1YDHMP9rEmzyNl1VjUQQmIyskjLuLF

**Importing Helper Library**
"""

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import  train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

"""**Importing Training and Test File** """

datapath = "./train.csv"
ogData = pd.read_csv(datapath)

testDatapath = "./test.csv"
ogTestData = pd.read_csv(testDatapath)

"""**Checking if data has NULL values or not** """

print(ogData.isnull().sum())
print(ogTestData.isnull().sum())

"""**Setting Original Data into New Variable, so that Original Data can't be Alter** """

data = ogData
testData = ogTestData

"""**Printing Unique Values of Data** """

for i in data:
  print(i, data[i].unique())

"""**Defining A Function Which Set the NULL Values to Median** """

def ReplaceMissingMedian(col,dataset):
  median = round(dataset[col].median())
  dataset[col].fillna(median, inplace=True)

"""**Defining A Function Which Set the NULL Values to Mode** """

def ReplaceMissingMode(col,dataset):
  mode = dataset[col].mode()
  dataset[col].fillna(mode, inplace=True)

"""**Calling ReplaceMissingMedian and ReplaceMissingMode to Replace NULL Values of Data** """

ReplaceMissingMode('HomePlanet',data)
ReplaceMissingMode('CryoSleep',data)
ReplaceMissingMode('Cabin',data)
ReplaceMissingMode('Destination',data)
ReplaceMissingMode('VIP',data)
ReplaceMissingMedian('Age',data)
ReplaceMissingMedian('RoomService',data)
ReplaceMissingMedian('FoodCourt',data)
ReplaceMissingMedian('ShoppingMall',data)
ReplaceMissingMedian('Spa',data)
ReplaceMissingMedian('VRDeck',data)

ReplaceMissingMode('HomePlanet',testData)
ReplaceMissingMode('CryoSleep',testData)
ReplaceMissingMode('Cabin',testData)
ReplaceMissingMode('Destination',testData)
ReplaceMissingMode('VIP',testData)
ReplaceMissingMedian('Age',testData)
ReplaceMissingMedian('RoomService',testData)
ReplaceMissingMedian('FoodCourt',testData)
ReplaceMissingMedian('ShoppingMall',testData)
ReplaceMissingMedian('Spa',testData)
ReplaceMissingMedian('VRDeck',testData)

"""**Fitting the LabelEncoder** """

a = data['Cabin'].unique()
b = testData['Cabin'].unique()
c = np.concatenate((a, b))
d = pd.Series(c).unique()

homePlanetLabel = LabelEncoder().fit(data['HomePlanet'])
cryoSleepLabel = LabelEncoder().fit(data['CryoSleep'])
cabinLabel = LabelEncoder().fit(d)
destinationLabel = LabelEncoder().fit(data['Destination'])
vipLabel = LabelEncoder().fit(data['VIP'])
transportedLabel = LabelEncoder().fit(data['Transported'])

"""**Replacing the data with LabelEncoder** """

data['HomePlanet'] = homePlanetLabel.transform(data['HomePlanet'])
data['CryoSleep'] = cryoSleepLabel.transform(data['CryoSleep'])
data['Cabin'] = cabinLabel.transform(data['Cabin'])
data['Destination'] = destinationLabel.transform(data['Destination'])
data['VIP'] = vipLabel.transform(data['VIP'])
data['Transported'] = transportedLabel.transform(data['Transported'])

testData['HomePlanet'] = homePlanetLabel.transform(testData['HomePlanet'])
testData['CryoSleep'] = cryoSleepLabel.transform(testData['CryoSleep'])
testData['Cabin'] = cabinLabel.transform(testData['Cabin'])
testData['Destination'] = destinationLabel.transform(testData['Destination'])
testData['VIP'] = vipLabel.transform(testData['VIP'])

"""**Checking if there are any Remaining NULL values** """

print(ogData.isnull().sum())
print(ogTestData.isnull().sum())

"""**Splitting Data into Features and Target Variable** """

"""['PassengerId', 'HomePlanet', 'CryoSleep', 'Cabin',
    'Destination', 'Age', 'VIP', 'RoomService', 'FoodCourt',
    'ShoppingMall', 'Spa', 'VRDeck', 'Name', 'Transported']"""

features = ['HomePlanet','CryoSleep', 'Cabin','Destination','Age','VIP',
            'RoomService','FoodCourt','ShoppingMall','Spa','VRDeck']
target = ['Transported']

filterData = data[features + target]

X = filterData.iloc[:,:-1]
Y = filterData.iloc[:,-1]
testFileData = testData[features]

X.head()

"""**Splitting Train Data into Train and Test Variables** """

train_X,val_X,train_Y,val_Y = train_test_split(X,Y,test_size=0.2,random_state=0)

print("Training Data: ", train_Y.count(),end="\n\n")
print("Validation Data: ", val_Y.count(),end="\n\n")

train_X.head()

"""**Testing how well RandomForestClassifier Performs** """

forestModel = RandomForestClassifier(n_estimators=256, random_state=0)
forestModel.fit(train_X,train_Y)

forestPredict = forestModel.predict(val_X)

print(confusion_matrix(val_Y,forestPredict))
print(classification_report(val_Y,forestPredict))

"""**Testing how well DecisionTreeClassifier Performs** """

treeModel = DecisionTreeClassifier(random_state=0)
treeModel.fit(train_X,train_Y)

treePredict = treeModel.predict(val_X)

print(confusion_matrix(val_Y,treePredict))
print(classification_report(val_Y,treePredict))

"""**Testing how well KNeighborsClassifier Performs** """

knn = KNeighborsClassifier(n_neighbors=7)
knn.fit(train_X,train_Y)

knnPredict = knn.predict(val_X)

print(confusion_matrix(val_Y,knnPredict))
print(classification_report(val_Y,knnPredict))

"""**Testing how well KMeans Performs** """

kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(train_X)

kmeansPredict = kmeans.predict(val_X)

print(confusion_matrix(val_Y,kmeansPredict))
print(classification_report(val_Y,kmeansPredict))

"""**Testing how well LogisticRegression Performs** """

logModel = LogisticRegression(random_state=0,max_iter=512)
logModel.fit(train_X,train_Y)

logPredict = logModel.predict(val_X)

print(confusion_matrix(val_Y,logPredict))
print(classification_report(val_Y,logPredict))

"""**Testing how well VotingClassifier Performs** """

voteModel = VotingClassifier(estimators=[('forest', forestModel),('tree', treeModel), ('log', logModel)])
voteModel.fit(train_X,train_Y)

votePredict = voteModel.predict(val_X)

print(confusion_matrix(val_Y,votePredict))
print(classification_report(val_Y,votePredict))

"""#Submission

**As RandomForestClassifier Performs Best from other Algorithm, we will retrain the model with the whole Train Dataset**
"""

model =  RandomForestClassifier(n_estimators=256, random_state=0)
model.fit(X,Y)

"""**Predicting the Values of Test Data from the Previously Train Dataset and Storing it in a DataFrame** """

passengerID = ogTestData['PassengerId']
predictedValue = model.predict(testFileData)

ans = transportedLabel.inverse_transform(predictedValue)

output = pd.DataFrame()
output['PassengerId'] = passengerID
output['Transported'] = ans

output

"""**Saving the Output DataFrame into a CSV File** """

output.to_csv('final_17.csv',index=False)