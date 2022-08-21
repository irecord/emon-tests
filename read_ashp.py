#!/usr/bin/python
from websocket import create_connection
import json, datetime, time, urllib

def ident(ws, to):
    msg = "{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/$to$\",\"fr\":\"/beep\",\"rqi\":\"blah\"}}"
    ws.send(msg.replace("$to$", to))
    result = json.loads(ws.recv())
    print(result)

def read(ws, to, debug):
    msg = "{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/$to$\",\"fr\":\"/beep\",\"rqi\":\"blah\"}}"
    ws.send(msg.replace("$to$", to))
    j = json.loads(ws.recv())
    if debug:
        print(j)
    r = j["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    print("{to}: {r}".format(to=to,r=r))
    return r

def main():
    ws = create_connection("ws://192.168.0.150/mca")
    #ident_0 = ident(ws, "0/UnitProfile/la")
    #ident_1 = ident(ws, "1/UnitProfile/la")
    #ident_2 = ident(ws, "2/UnitProfile/la")

    ashp_temp_lw = read(ws, "1/Sensor/LeavingWaterTemperatureCurrent/la", False)
    ashp_temp_in = read(ws, "1/Sensor/IndoorTemperature/la", False)
    ashp_temp_out = read(ws, "1/Sensor/OutdoorTemperature/la", False)
    ashp_power = read(ws, "1/Operation/Power/la", False)

    tank_temp = read(ws, "2/Sensor/TankTemperature/la", False)
    tank_power = read(ws, "2/Operation/Power/la", False)
    tank_immersion_on = read(ws, "2/Operation/Powerful/la", False)
    tank_target = read(ws, "2/Operation/TargetTemperature/la", False)
    tank_temp_max = read(ws, "2/Operation/DomesticHotWaterTemperatureHeating/la", False)

if __name__ == "__main__":
  main()
