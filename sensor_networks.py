# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 01:37:27 2019

@author: Kribshan Naidoo

Summative Assessment

git repo link: https://github.com/Kribashan/sensornetworks.git

ssh git repo link: git@github.com:Kribashan/sensornetworks.git
"""

import random
import csv
import os
import datetime
import logging
#import time

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(filename='SensorErrorLog.log',level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def GenerateData ():
    outputData = []
    sensors = []
    for i in range(0,32):
        for j in range(0,16):
            sensors.append(float('%.4f'%random.random()))
        outputData.append(sensors)
        sensors = []
    return outputData

def MakeDict(dataset):
    data = {}
    for k, v in enumerate(dataset):
        data[k+1] = v
    return data

def GenerateError (data):
    no_err = random.randrange(10)
    
    for i in range(no_err):
        cluster = random.randrange(1, 32, 1)
        sensor = random.randrange(1, 16, 1)
        data[cluster][sensor] = 'err'

def CheckForErr(data):
    listErr = {}
    for k, v in data.items():
        if (-1 in v):
            for i,x in enumerate(v): 
                if (x == -1):
                    listErr[k] = i
    return listErr

def ReplaceError(data):
    for k, v in data.items():
        if ('err' in v):
            for i,x in enumerate(v): 
                if (x == 'err'):
                    data[k][i] = -1
    return data

def WriteData(data):
    path = os.getcwd()  
    data['timestamp'] = datetime.datetime.now()    
    exists = os.path.isfile(path + '\\DataArchive.csv')    
    if exists:
        with open('DataArchive.csv', 'a') as csvfile:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)
    else:
        with open('DataArchive.csv', 'w') as csvfile:
            fieldnames = data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data)
        
#count = 0
#print("Time start: {}".format(datetime.datetime.now()))
#while(count < 5):
    
data = {}
dataIn = []
message = ''
dataIn = GenerateData()

data = MakeDict(dataIn)

GenerateError(data)
data = ReplaceError(data)
errorlist = CheckForErr(data)

if (len(errorlist) != 0):
    for k, v in errorlist.items():
        message = message + 'Cluster: {0} has error on sensor: {1} \n'.format(k,v)
    logging.warning(message)

WriteData(data)
#    count += 1
#    time.sleep(0.1)
#print("Time stop: {}".format(datetime.datetime.now()))