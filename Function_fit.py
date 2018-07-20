# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 13:54:16 2018

@author: marco
"""

"""FIT PROCEDURE IN PYTHON"""
"""VERSION 0.5"""

#GENERATE RANDOM DATA

import numpy as np # import math library
np.random.seed(0) # Seed the random number generator for reproducibility
x_data = np.linspace(-5, 5, num=50) #Create a vector of 50 elements between -5 and 5
y_data = np.sin(x_data) + 0.2*np.random.normal(size=50) #Create a sinusoidal sequence with noise

#FIT A FUNCTION TO THE DATA

from scipy import optimize #import optimization library
def test_func(x,a,b):
    return a*np.sin(b*x) #define a test function
p, p_cov= optimize.curve_fit(test_func, x_data, y_data, p0=[1, 1])#fit the data with the test function using the initial parameter 1 and 1
p_err=(p_cov[0][0]**0.5, p_cov[1][1]**0.5) #the square root of covariance diagonal elements is an indication of the error in the parameters
print(p, p_err) #print out the results

#PLOT THE DATA, THE FIT AND THE RESIDUES

import matplotlib.pyplot as plt #import plot library
fig1 = plt.figure(1) #define the figure
frame1=fig1.add_axes((.1,.3,.8,.6)) #xstart, ystart, xend, yend [units are fraction of the image frame, from bottom left corner]
#plt.figure(figsize=(6, 4)) #chose the domensions of the plot
plt.scatter(x_data, y_data, label='Data') #plot the data
plt.plot(x_data, test_func(x_data, p[0], p[1]), label='Best fit function') #plot the test function with the fitted parameter
plt.plot(x_data, test_func(x_data, p[0]+p_err[0], p[1]+p_err[0]), label='Upper extreme') #plot function with parameters plus error
plt.plot(x_data, test_func(x_data, p[0]-p_err[0], p[1]-p_err[0]), label='Lower extreme') #plot function with parameters less error
plt.legend(loc='best') #put the legend in the best position
frame1.set_xticklabels([]) #Remove x-tic labels for the first frame
plt.grid() #put grid on the plot
difference = y_data-test_func(x_data, p[0], p[1]) #claculate the residuals
y_zeros=np.zeros(50) #make a vector for the zero residue line
frame2=fig1.add_axes((.1,.1,.8,.2)) #create the second frame of the residuals plot
plt.plot(x_data,difference,'or') #Residual plot
plt.plot(x_data,y_zeros) #plot the line with zero residue
plt.grid() #put a grid on the plot
plt.show() #show the plot

