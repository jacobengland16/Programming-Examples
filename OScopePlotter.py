"""
Created on Fri Jun  1 13:51:03 2018

@author: jengland
"""


'''
The script was used for an experiment where an oscilloscope was used to
collect a signal. The corresponding values of the signal were exporded as a CSV
and plotted using the script below. 

The signal was rather messy, so smoothing was done using a gaussian smoothing technique

'''
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

##using a gaussian smoothing technique to smooth signal
def plotSmoothRingout(yList,smooth_r = 3):
    gauss_YList = signal.gaussian(smooth_r*8+1,smooth_r)
    yPoints = signal.correlate(yList,gauss_YList/np.sum(gauss_YList),mode="same")
    return yPoints

#smooth the fourier transform of the signal
def plotSmoothFFT(yList, smooth_r = 3):
    yfft = np.abs(np.fft.fft(yList))
    gauss = signal.gaussian(smooth_r*8+1,smooth_r)
    yfft = signal.correlate(yfft,gauss/np.sum(gauss),mode="same")
    return yfft

def main():
    #change fileName based on which file you want to read from. change legendLabel to name of function
    fileName = 'NewFile3.csv' 
    legendLabel = "Linear"
    
    #declare the start time and step time, used to generate x-values
    increment = 1.00*10**-2
    start = -5.44*10**0
    
    #generate list of y values
    yList = np.genfromtxt(fileName,delimiter=',',skip_header = 2)[:,0]
    #calculate the end time
    end = (increment*(len(yList)))+ start
    #generate a list of x values
    xList = np.linspace(start,end,len(yList))
    #calcualte the sample rate, used to find frequency
    sampleRate = 1/(increment)
    freq = np.arange(len(yList))*sampleRate/len(yList)

    #Volts vs. Time Graph
    plt.figure(1)
    plt.grid()
    plt.minorticks_on()
    plt.title(("Volts vs. Time: {0}").format(legendLabel))
    plt.xlabel("Time (s)")
    plt.ylabel("Volts")
    yValues = plotSmoothRingout(yList)
    plt.plot(xList,yValues, label = legendLabel)
    plt.legend()
    plt.show()

    #fft plot
    plt.figure(2)
    plt.grid()
    plt.minorticks_on()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title(("FFT - {0}").format(legendLabel))
    plt.xlim([0,2.5*(10**4)])
    yFFTValues = plotSmoothFFT(yList)
    plt.plot(freq,yFFTValues,label = legendLabel)
    plt.legend()

    plt.show()
    
main()