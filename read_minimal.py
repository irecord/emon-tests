#!/usr/bin/env python3
import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 200)  # port name, slave address (in decimal)

instrument.serial.baudrate = 9600         # Baud
instrument.serial.bytesize = 8
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.05          # seconds

instrument.address = 2                         # this is the slave address number
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode

## Read temperature (PV = ProcessValue) ##
temperature = instrument.read_register(289, 1)  # Registernumber, number of decimals
print(temperature)

