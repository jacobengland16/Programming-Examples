"""
Created on Mon Dec  3 19:32:14 2018
@author: Jacob England

## Script to draw Mohr's Circle
## User enters initial stress conditions and angle to rotate element. 
## Blue point is stress in X, green Point is stress in Y. 
## Principle stress are denotated with black dots. The red point will
## denote the initial stress condition. 
"""

import matplotlib.pyplot as plt
import numpy as np

print("Enter the units and initial stresses to draw Mohr's Circle. Be sure to use the correct sign convention!")

#asking for inputs
sigmaX = input("Enter the initial stress in X-direction: ")
sigmaY = input("Enter the initial stress in Y-direction: ")
tau = input("Enter the initial shear stress: ")
angle = input("Enter the rotation angle: ")

#float inputs, input saves everything as a string
sigmaX = float(sigmaX)
sigmaY = float(sigmaY)
tau = float(tau)
angle = float(angle)

angle2 = angle * 2
radianAngle = np.deg2rad(angle2)

#calculations to find needed info
####---------------------------------------------
averageStress = (sigmaX + sigmaY)/2

averageDiff= ((sigmaX - sigmaY)/2)**2
tauSquared = tau ** 2

radius = np.sqrt(averageDiff + tauSquared)

minX = ((averageStress - radius) - 5)
maxX = averageStress + radius + 5
minY = -1 * (radius + 5)
maxY = radius + 5

principleStress1 = averageStress - radius
principleStress2 = averageStress + radius

##calculate transformed stresses. 
transX = (averageStress + (((sigmaX - sigmaY)/2)*(np.cos(radianAngle)))+(tau*(np.sin(radianAngle))))
transY = (averageStress - (((sigmaX - sigmaY)/2)*(np.cos(radianAngle)))-(tau*(np.sin(radianAngle))))
transTau = (((-1*((sigmaX - sigmaY)/2))*np.sin(radianAngle)) + (tau*np.cos(radianAngle)))

####---------------------------------------

#sets up the conditions for the graph. titles, limits, axis, etc
fig = plt.figure()
fig.add_subplot()
fig.set_size_inches(10,10)
ax = plt.gca()
ax.set_aspect("equal")
ax.set_title("Mohr's Circle")
ax.set_xlabel("sigma")
ax.set_ylabel("tau")
ax.grid(True)
ax.set_xlim(minX,maxX)
ax.set_ylim(minY,maxY)
ax.invert_yaxis()

#graphs the cricle
mohrsCircle = plt.Circle((averageStress,0),radius = radius, color = "b",fill = False,label = "mohrs circle")

#plots the extreme points, top, bottom, left, and right
ax.plot(averageStress,0,"o",color = "black")
ax.plot(principleStress1, 0, "o",color = "black",label = "Principle Stress")
ax.plot(principleStress2, 0, "o",color = "black")
ax.plot(sigmaX,tau,"o",color = "red",label="Initial Point")#initial stress point
ax.plot(transX,transTau,"o",color = "blue")
ax.plot(transY,-1 * transTau,"o",color = "green")
ax.plot([transY,transX],[-1*transTau,transTau],color = "green",label = "Transformed Stress")

#annotate the points, i.e. tells what point they're at
ax.annotate("  ({},0)".format(principleStress1),xy = (principleStress1,0))
ax.annotate("  ({},0)".format(principleStress2),xy = (principleStress2,0))
ax.annotate("({},{})".format(averageStress,radius),xy = (averageStress,radius))
ax.annotate("({},{})".format(transX,transTau),xy = (transX,transTau))
ax.annotate("{},{}".format(transY,-1 * transTau),xy = (transY,-1 * transTau))
ax.legend(loc = "best")
ax.add_artist(mohrsCircle)
fig.savefig("plot.png")