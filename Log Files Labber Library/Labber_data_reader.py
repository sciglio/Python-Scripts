# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:29:39 2018

@author: scmarco
"""

"""READ GENERIC LABBER DATA"""
"""VERSION 0.1"""

import Labber #installing Labber this library is present in “Script” folder of the main program directory (add this folder to python PATH)
import numpy as np #math library
import matplotlib.pyplot as plt #plot library

#the LOGFILE is composed by:
#ENTRY : a single measure in the step configuration that contains the intruments names, their output, the log channels and their output. 
#Each step in the step configuration is an entry except for the first one that produces a vector.
#LOG CHANNELS: the names of the values that the intruments read and logged. If these values are vectors, their dimension is the same of the first step


f=Labber.LogFile('MS_rabi_12_Aover10') #read a hdf5 file with measurement data

#Simple functions that read textual part

user=f.getUser() #read the user that log the measurement
tag=f.getTags() #read the tags
project=f.getProject() #read the project name
comment=f.getComment() #read the comment
print('User:'), unicode(user) #print the user
print('Tag:'), unicode(tag) #print the tag
print('Projrct:'), unicode(project) #print the project name
print('Comment:'), unicode(comment) #print the comment


"""Functions that read the data structure"""

NE=f.getNumberOfEntries() #read number of entries, i.e. all different measurements 
StepChannels=f.getStepChannels() #return a dictionary with all the steps in the step channels windows used during the measurement
steps=len(StepChannels)
NL=f.getNumberOfLogs() #


"""Functions that read data"""

data=f.getEntry(0) #it returns a dictionary with the steps names as the keys
channels=f.getLogChannels() #read the n log steps and return a list of n dictionaries



"""Read a generic file"""

#READ HOW MANY CHANNELS AND GIVE THEM A NAME 
channels=f.getLogChannels() #read the n steps and return a list of n dictionaries
Nchannels=len(channels) #number of log channels
nameChannels=[] #generate an empty list for the channels name
for i in range (Nchannels):
    nameChannels.append(channels[i].get('name'))
print('The Log Channels are:')
for i in range(Nchannels):
    print nameChannels[i]


#READ HOW MANY ENTRIES AND LINK THEM TO THE STEP CHANNELS
NE=f.getNumberOfEntries() #read number of entries, i.e. all different measurements 
realSteps=0 #define a variable for the swepped steps
for i in range(steps):
    if len(StepChannels[i].get('values'))>1:
        realSteps+=1
lenSteps=realSteps*[0] #define a list for each step length 
stepEntries=1   #define a variable for the expected entries according to the steps channels
for i in range(realSteps):
    lenSteps[i]=len(StepChannels[i].get('values'))
    if i>0: #the first step produces the vector, it is not an entry
        stepEntries*=lenSteps[i]
#check that the measurement works 
if NE!=stepEntries:
    print'WARNING! Expected ', stepEntries, ' entries. Found only ', NE
    print 'This measure has been stopped before it was completed. Be carefull with data handling.'
    NE=NE-1 #remove the last entry by defaoult (it very likely to be uncomplete)

#CREATE A STRUCTURE FOR THE DATA: VALUES[LOG_CHANNEL][#ENTRIES][Npoints]
Npoints=len(StepChannels[0].get('values')) #the first step channel determines the length of the vector
ValuesX=np.zeros((Nchannels,Npoints)) #the X axis is the same for all the entries
data=f.getEntry(0) #use the first entries to determine if the data are real or complex
#Check if the data are real or complex in order to create the array
if np.iscomplexobj(data.get(nameChannels[0])):
    ValuesY=np.zeros((Nchannels,NE,Npoints))+1j*np.ones((Nchannels,NE,Npoints))
else:
    ValuesY=np.zeros((Nchannels,NE,Npoints))
#store the data in the array just created
for i in range(Nchannels):
    for j in range(NE):
        data=f.getEntry(j)
        ValuesY[i][j]=data.get(nameChannels[i])
    ValuesX[i]=StepChannels[0].get('values')


#AVERAGING AND PLOT DATA
plt.plot(ValuesX[0],np.abs(np.mean(ValuesY[0], axis=0)))





plt.show()
    
