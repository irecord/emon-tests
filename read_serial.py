#!/usr/bin/python
import threading, time, subprocess, logging, minimalmodbus, serial, struct
from time import sleep

def read():
  ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

  num, = struct.unpack('<H', ser.read(2))
  part = format(num, '04x')
  packet = part
  if part == '0302':
    num, = struct.unpack('<H', ser.read(2))
    part = format(num, '04x')
    while part != '0302':
      packet = packet + ' ' + part
      num, = struct.unpack('<H', ser.read(2))
      part = format(num, '04x')

  print packet

def main():
  while True:
    read()

if __name__ == "__main__":
  main()

