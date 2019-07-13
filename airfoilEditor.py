"""
@author: Jacob England
"""

#This Program is used to correctly format and size data points of an airfoil.
#Online airfoils are for a generic size, and only include x and y data points.
#This program also gives a feature to offset the foils location within Solidworks.
#SolidWorks also requires z points. The airfoils generated online also can't
#easily size the airfoils, and doesn't include z data points.
#This program gives us an easy and consolidated method of doing these tasks. 


import numpy as np

def main():
    
    #open specific fileName.. Multiply the points by some constant to get the
    #correct size. z array is used to add a specific number of 0's. This is 
    #done because Solidworks requires x,y, and z data points. Change x and y
    #offset to alter location that the foil is located.
    
    fileName = "naca0009.txt"
    constant = 6.5
    xOffset = 0
    yOffset = 0
    zOffset = 0
    
    z = []
    
    x = np.genfromtxt(fileName, delimiter = None, skip_header = 1)[:,0]
    y = np.genfromtxt(fileName, delimiter = None, skip_header = 1)[:,1]
    
    #generate correct number of zeros to be saved to the .csv file
    for i in range(0,len(x)):
        z.append(zOffset)
    
    #multiply the x and y list by the constant and add offset
    x = (x * constant) + xOffset
    y = (y * constant) + yOffset
    
    #saved generated data points to a .txt file. saved in same place as script 
    np.savetxt('naca0009_6.5.txt',np.transpose([x,y,z]),delimiter = ",")

main()