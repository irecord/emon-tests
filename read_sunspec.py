#!/usr/bin/env python3
import sunspec2.modbus.client as client

d = client.SunSpecModbusClientDeviceRTU(slave_id=2, name="/dev/ttyUSB0")

print(d.models)
