#!/usr/bin/python
import threading, time, subprocess, logging, minimalmodbus
from time import sleep
wattson = minimalmodbus.Instrument("/dev/ttyUSB0", 2)
wattson.serial.baudrate = 9600
wattson.serial.bytesize = 8
wattson.serial.parity = minimalmodbus.serial.PARITY_NONE
wattson.serial.stopbits = 1
wattson.serial.timeout = 1
wattson.mode = minimalmodbus.MODE_RTU
logging.basicConfig()

def read_meter():

  TEC  = round(wattson.read_float(768), 3) # total energy consumed KWh
  CONS = int(wattson.read_float(770)*1000) # total real power Watts
  VOLT = round(wattson.read_float(792), 1) # voltage
  LEG1 = int(wattson.read_float(806)*1000) # watts A
  #LEG2 = int(wattson.read_float(808)*1000) # watts B
  #GENW = int(wattson.read_float(810)*1000) # watts C (PV output)
  IMPA = round(wattson.read_float(832), 3) # import A KWh
  #IMPB = round(wattson.read_float(834), 3) # import B KWh
  EXPA = round(wattson.read_float(840), 3) # export A KWh
  #EXPB = round(wattson.read_float(842), 3) # export B KWh
  NETA = round(wattson.read_float(848), 3) # net A KWh
  #NETB = round(wattson.read_float(850), 3) # net B KWh
  #NETC = round(wattson.read_float(852), 3) # net C KWh
  #HTOT = LEG1 + LEG2

#  if GENW < 50: # if PV output < 50 Watts set it to zero Watts
#     GENW = 0

  file = open('/tmp/meter_data.txt', 'w+')
  file.write(time.strftime('%Y%m%d %X '))
  file.write('{} {} {} {} {} {}\n'.format(VOLT,CONS,TEC,IMPA,EXPA,NETA))
  file.close()

#  subprocess.call('/opt/send-to-eorg.sh') # call the bash file to transmit the data

def main():
  read_meter()

  while True:
    sleep(1)

if __name__ == "__main__":
  main()

