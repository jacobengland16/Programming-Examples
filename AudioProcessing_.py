# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:49:37 2019

@author: jengland
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import scipy.signal as sp

'''
Code was used as a method to process audio data
'''

'''
Available functions:
    
    - Load and Normalize Audio Data
    - Plot the Scale Data
    - Create Spectrograms of the Audio (graphed with identical scaling of amplitude)
    - Plot the raw Audio (time domain)
    - Plot the normalized audio (time domain)
    - very simple method of plotting a single seed impact
    - Plot of Fourier Transform
    - Plot the average of fourier transform (useful for plotting several FT's on same graph for comparrison)
    
'''


#generates a list of scale data from a specified directory
def getScale(directory):
    scaleList = glob.glob(directory+"/*_Scale.csv")
    return scaleList

#generates a list of audiofiles from a specified directory
def getAudio(directory):
    audioList = glob.glob(directory+"/*.npy")
    return audioList

#loads each data file, normalizes 
def load_and_normalize(fileName, timeStart = 0, timeEnd = 30,fs = 48000):
    #can choose to only load part of the file using timeStart and timeEnd, the corresponding sample number is computed
    sampleStart = int(round(fs*timeStart))
    sampleEnd = int(round(fs*timeEnd))
    
    y = np.load(fileName)   #loads file
    y = y[sampleStart:sampleEnd]    #chooses which data points to take based on start and end times
    y = y.astype('float')
    y = y - np.mean(y)  
    m = max(abs(np.max(y)), abs(np.min(y)))
    y = y/m        
    return y

#calculates the necessary information to properly create spectrogram. 
#to compare spectrograms, the max and min values must be found for the entire data set
def specGramInfo(audioList,fs = 48000):    
    #create two empty arrays
    Sxx_min = []
    Sxx_max= []
    
    #loops through every file in the audio list
    for i in audioList:
        x = load_and_normalize(i)
        
        #creates spectrogram
        f, t, Sxx = sp.spectrogram(x, fs=fs)
        logsxx = np.log(Sxx)
        
        #find max and min value in specific audio file
        minValue = np.min(logsxx)
        maxValue = np.max(logsxx)
        
        #append these values to an array
        Sxx_min = np.append(Sxx_min,minValue)
        Sxx_max = np.append(Sxx_max,maxValue)
     
    #find the total max and min values for the data set
    vmin = np.min(Sxx_min)
    vmax = np.max(Sxx_max)
        
    return vmin, vmax

#plots the scale data with time (weight vs time)
def plotScale(directory):
    
    #call getData to get list of file names
    scaleList = getScale(directory)
    
    #for every file in the list, create a unique plot
    for i in scaleList:
        plt.figure(i)
        scaleData = np.genfromtxt(i,delimiter = ',') #generate data from .csv file
        time = scaleData[:,0] #take all data in first column (time values)
        weight = scaleData[:,1] #take all data in second column (weight values)
        
        #create plots and titles
        plt.plot(time,weight)
        plt.title(i)
        plt.xlabel("Time (s)")
        plt.ylabel("Weight (g)")
        
#plots the raw audio. plots the first 100000 samples
def plotAudio_Raw(directory):
    audioList = getAudio(directory)
    #need a modification of getData to get the names of the audio files, can get
    #creative about how we want to analyze data
    
    for i in audioList:
        plt.figure(i)
        y = np.load(i)
        plt.plot(y)
  
#plots the audio in the time domain. can specify what time values      
def plotAudio_Time(directory, fs = 48000,startTime = 0, endTime = 30):
    #get list of audio files contained in local directory
    audioList = getAudio(directory)
    
    
    #for every data file in the list, creates a graph
    for i in audioList:
        plt.figure()
        #load and normalize data of each audio file
        y = load_and_normalize(i,timeStart = startTime, timeEnd = endTime)
        x = np.linspace(0+startTime, (len(y) / fs) + (startTime), len(y))   #create x values
        plt.plot(x,y)
        plt.xlim([startTime,endTime])
        plt.ylim([-1,1])
        plt.title(i)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude - Normalized")
     
#generates a spectrogram of all data in the specified directory
def specGram(directory, fs = 48000, startTime = 0, endTime = 30):
    audioList = getAudio(directory)
    vmin, vmax = specGramInfo(audioList)
    
    for i in audioList:
        plt.figure()
        y = load_and_normalize(i,timeEnd = endTime)
        f, t, Sxx = sp.spectrogram(y, fs=fs)
        logsxx = np.log(Sxx)
        plt.title(i)
        plt.xlim(startTime,endTime)
        plt.xlabel("Time (seconds)")
        plt.ylabel("Frequency (Hz)")
        plt.pcolormesh(t, f, logsxx, vmin = vmin, vmax = vmax)
   
    
#graph individual seed impact from a specified file.
        
#this function will require some tweaking to get working correctly. 
#the function just chooses all information around an impact exceeding a certain 
#value. if several impacts occur in a very short time, the function may grab several impacts. 
def hit(endTime,searchAmplitude,audioFile, startTime = 0, fs = 48000):
    #find the number of samples to move forward and back once the desired magnitude is detected
    backTime = .0018
    forwardTime = .015
    backSamples = int(round(fs*backTime))
    forwardSamples = int(round(fs*forwardTime))
    
    #load and normalize the data from the specified file
    y = load_and_normalize(audioFile,timeEnd = endTime)

    #loops through the list of audio data, 
    #starts at the sample representing (starting) sec, ends at sample representing(ending) sec
    for i in range(fs*startTime,fs*endTime):
        if y[i] > searchAmplitude:  #loop will continue until amplitude exceeds a specified value
            y = y[i-backSamples:i+forwardSamples]
            break #for loop breaks once it finds value exceeding serach amplitude
            
    #if no value greater than the serachAmplitude was found, print an error message
    else: 
        print('No impacts of this amplitude or gretaer.')
    
    x = np.linspace(0, (len(y) / fs)*1000, len(y))
    z = np.zeros(len(y))

    plt.figure() #create figure 
    plt.plot(x,y,x,z)
    plt.xlim([0,(len(y)/fs)*1000])
    plt.title(audioFile)
    plt.xlabel("Ringout Time (s)")
    plt.ylabel("Amplitude - Normalized")
    plt.show()

#take the Fourier transform of every file in the audio list. start and end time can be specified
def fft(directory, fs = 48000,startTime = 0, endTime = 30):
    audioList = getAudio(directory)
    
    for i in audioList:
        y = load_and_normalize(i,timeStart = startTime, timeEnd = endTime)
        freq = np.arange(len(y))*(fs/len(y))
        #yfft = np.abs(np.fft.fft(y))
        yfft = (np.fft.fft(y))
        plt.figure()
        plt.plot(freq[0:int(len(freq)/2)],yfft[0:int(len(freq)/2)])
        plt.title(i)
        plt.xlabel("Frequency (Hz)")

#function to take short time Fourier transform of function. the fourier transform
#data for each time step will be averaged. This is done to elimate unncessacry content 
def fftAverage(directory,fs = 48000, timeStep = 1, startTime = 0, endTime = 30):
    
      #to calculate the short time fourier transform, a time step is initally needed.
      #after this, a matrix is created, with a number of rows equal to how many time steps 
      #are necessary to include the entire test, and a number of columns equal to the number
      #of samples that's included in each time step. These rows of the matrix are then averaged
      #to give an "average" value of the Fourier transform.
    audioList = getAudio(directory)
    
     #check to reset the time step if necessary. code currently breaks with time step < 1. 
    if isinstance(timeStep,int) == 0:
         timeStep = 1
         print("timeStep must be an int. the value was set to a default")
         
    plt.figure()
         
    for k in audioList:
         y = load_and_normalize(k)       #load and normalize audio data
         length = len(y)
         samplesPerSec = int((length/(endTime-startTime)))      #computes the number of samples per second
         samplesPerStep = int(samplesPerSec*timeStep)      #computes the number of samples per step

           
         yArray = np.empty(((int((endTime - startTime)/timeStep)),int(samplesPerStep)),float)   #create an array to store y-values
         yfft = np.empty(((int((endTime-startTime)/timeStep)),int(samplesPerStep)),float)       #create an array to store yfft-values
         
         #computes total time to calculate the number of steps required. 
         totalTime = endTime - startTime
         numSteps = totalTime/timeStep
         
         
         i = 0                  #---  declare counter variables ---#      
         timeCounter = 0        #---                            ---#
         while i < numSteps:
             yArray[i] =  y[int(timeCounter*samplesPerSec):int(((timeCounter+timeStep)*samplesPerSec))]            
             yfft[i] = np.abs(np.fft.fft(yArray[i]))       
           
             timeCounter = timeCounter + timeStep
             i = i + 1
           
            
         fft = np.mean(yfft,axis = 0) #average the rows of the yfft matrix, resulting in an array. 
         
         freq = np.arange(len(fft))*(fs/len(fft))   #create x values to plot Fourier transform
         plt.plot(freq[0:int(len(freq)/2)],fft[0:int(len(freq)/2)])
         plt.title(i)

        
def main():
    plotScale("C:\\Users\jengland\Desktop\\Seed")
    #plotAudio_Raw("C:\\Users\jengland\Desktop\\")
    #plotAudio_Time("C:\\Users\jengland\Desktop\\",fs = 48000,startTime = 1, endTime = 30)
    #specGram("C:\\Users\jengland\Desktop\\",startTime = 0,endTime = 3)
    #fft("C:\\Users\jengland\Desktop\\)
    #fftAverage("C:\\Users\jengland\Desktop\\")
main()