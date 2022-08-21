#!/usr/bin/env python3
#!/usr/bin/python
from websocket import create_connection
import json
import requests

def read(ws, to):
    msg = "{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/$to$\",\"fr\":\"/beep\",\"rqi\":\"blah\"}}"
    ws.send(msg.replace("$to$", to))
    j = json.loads(ws.recv())
    r = j["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    print("{to}: {r}".format(to=to,r=r))
    return r

def main():
    ws = create_connection("ws://192.168.0.150/mca")

    ashp_temp_lw = read(ws, "1/Sensor/LeavingWaterTemperatureCurrent/la")
    ashp_temp_in = read(ws, "1/Sensor/IndoorTemperature/la")
    ashp_temp_out = read(ws, "1/Sensor/OutdoorTemperature/la")

    tank_temp = read(ws, "2/Sensor/TankTemperature/la")
    tank_immersion_on = read(ws, "2/Operation/Powerful/la")
    tank_target = read(ws, "2/Operation/TargetTemperature/la")

    export = {} # The values that will be sent to emoncms

    export["ashp_temp_lw"] = ashp_temp_lw
    export["ashp_temp_in"] = ashp_temp_in
    export["ashp_temp_out"] = ashp_temp_out
    export["tank_temp"] = tank_temp
    export["tank_immersion_on"] = tank_immersion_on
    export["tank_target"] = tank_target

    print(json.dumps(export, indent=4))

    r = requests.post("http://localhost/input/post?node=daikin&apikey=b215641cf41c8ed618172ec7911f566c&data=" + json.dumps(export))
    print(r.status_code)
    print(r.text)
    if r.text != "ok":
        print(r.json())

if __name__ == "__main__":
  main()
