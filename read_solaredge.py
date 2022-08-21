#!/usr/bin/env python3

import requests
import json

import solaredge_modbus

if __name__ == "__main__":
    inverter = solaredge_modbus.Inverter(
        device="/dev/ttyUSB0",
        baud=115200,
        timeout=30,
        unit=2
    )

    export = {} # The values that will be sent to emoncms

    values = {} # All the values for detailed output
    values = inverter.read_all()
    meters = inverter.meters()
    batteries = inverter.batteries()
    values["meters"] = {}
    values["batteries"] = {}

    for meter, params in meters.items():
        meter_values = params.read_all()
        values["meters"][meter] = meter_values
        export[meter.replace("Meter","M") + "_power_ac"] = meter_values["power"] * 10 ** meter_values["power_scale"]

    for battery, params in batteries.items():
        battery_values = params.read_all()
        values["batteries"][battery] = battery_values
        battery_name = battery.replace("Battery","B")
        export[battery_name + "_power_ac"] = battery_values["instantaneous_power"]
        export[battery_name + "_temp"] = battery_values["average_temperature"]
        export[battery_name + "_available"] = battery_values["available_energy"]
        export[battery_name + "_max"] = battery_values["maximum_energy"]
        export[battery_name + "_soh"] = battery_values["soh"]
        export[battery_name + "_soe"] = battery_values["soe"]
        export[battery_name + "_status"] = battery_values["status"]

#    print(json.dumps(values, indent=4))

    export["I_power_ac"] = values["power_ac"] * 10 ** values["power_ac_scale"]
    export["I_power_dc"] = values["power_dc"] * 10 ** values["power_dc_scale"]
    export["I_temp"] = values["temperature"] * 10 ** values["temperature_scale"]

    print(json.dumps(export, indent=4))

    r = requests.post("http://localhost/input/post?node=solaredge&apikey=b215641cf41c8ed618172ec7911f566c&data=" + json.dumps(export))
    print(r.status_code)
    print(r.text)
    if r.text != "ok":
        print(r.json())
