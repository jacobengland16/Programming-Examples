"""
Created on Mon Jan  7 09:06:12 2019

@author: jengland
"""

#connect to B&K Precision Power Supply
import serial
import serial.tools.list_ports

#create list of all serial ports
ports = serial.tools.list_ports.comports()

#loop through list of ports. we search the description using "port.description"
#if we get a match, break out of both loops.
for port in ports:
    if "Silicon Labs" in port.description:
        connectPort = port.device
        break
    break

#create serial port object
serialPort = serial.Serial(connectPort, 9600, timeout = 1)

#if serial port isn't open, open it
if(serialPort.isOpen() == False):
    serialPort.open()

#encode voltage and current value to bytes
voltageControl = "VOLT120\r".encode()
currentControl = "CURR025\r".encode()

#write voltage and current. writing "GETD" will return the display voltage, 
#current and status reading from the PSU
serialPort.write(voltageControl)
ret1 = serialPort.read(10)

serialPort.write(currentControl)
ret2 = serialPort.read(10)

serialPort.write("GETD\r".encode())
ret3 = serialPort.read(100)

#close the port
serialPort.close()