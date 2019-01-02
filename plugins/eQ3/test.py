import os, sys

sys.path.append('/usr/local/lib/python3.6/dist-packages')
import pexpect
import json


class eQ3Plugin:
    enabled = False
    data = None

    def __init__(self):
        return

    def updateData(self, data):
        print("Temp: " + str(data["temperature"]))

    def onHeartbeat(self):
        try:
            mac = "00:00:00:00:00"
            print('current directory :' + str(pexpect.run('pwd')))
            result = pexpect.run('./eq3.exp ' + mac + ' json')
            data = json.loads(result.decode("utf-8"))
            self.updateData(data)
        except Exception as e:
            print(e)
            data = json.load(open('test_eq3.json'))
            self.updateData(data)


global _plugin
_plugin = eQ3Plugin()

_plugin.onHeartbeat()

# mac = "00:1A:22:08:00:1D"
# child = pexpect.run('/home/pi/eq3/eq3.exp '+mac+' json')
# hw = '/home/pi/eq3/eq3.exp'
# child = pexpect.spawn( hw , cwd=os.path.dirname(hw))
# child.sendline(' '+mac+' json')
# child.logfile = sys.stdout
# str_json = child.decode("utf-8")
# data = json.loads(str_json)
# print("Temp: " + str(data["temperature"]))
