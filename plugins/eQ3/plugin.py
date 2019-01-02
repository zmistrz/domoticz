# eQ3 Bluetooth Python Plugin
# https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
# pip install pexpect
# pip3 instll ptyprocess
# /usr/local/lib/python3.5/dist-packages/
# Author: Paweł Zawisza
#
"""
<plugin key="eQ3Bth" name="eq3 Bluetooth Python Plugin" author="pzawisza" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://pawel-zawisza.pl/">
    <params>
     <param field="Address" label="Adres MAC" width="200px" required="true" default="00:00:00:00:00:00"/>
    </params>
</plugin>
"""
import os,sys
sys.path.append('/usr/local/lib/python3.6/dist-packages')
import Domoticz
import ptyprocess
import json
import pexpect
import time

class eQ3Plugin:
    enabled = False
    data = None
    plugin_path = '/home/domoticz/domoticz/plugins/eQ3'
    def __init__(self):
        #self.child = pexcept.spawn('/usr/bin/gattool -I')

        return
    # https://github.com/domoticz/domoticz/blob/development/hardware/hardwaretypes.h
    def onStart(self):
     Domoticz.Log("onStart eQ3 called")
     #Devices[1].Delete()
     #Devices[2].Delete()
     #Devices[3].Delete()
     #Devices[4].Delete()
     #Devices[5].Delete()

     if (len(Devices) == 0):
       Domoticz.Device(Name="na głowicy",Unit=1,Type=242,Subtype=1).Create()
       Domoticz.Device(Name="w pokoju",Unit=2,Type=242,Subtype=2).Create()
       Domoticz.Device(Name="otwarcie głowicy", Unit=3, Type=243,Subtype=6).Create()
       myOptions = {"LevelActions": "Off|10|20|30|40",
                  "LevelNames": "Off|Maksimum|Test|Manualny|Auto",
                  "LevelOffHidden": "false",
                  "SelectorStyle": "0"}
       Domoticz.Device(Name="Tryb pracy", Unit=4, Type=244,Subtype=62,Options=myOptions).Create()
       Domoticz.Device(Name="Tryb pracy", Unit=4, TypeName="Selector Switch", Options=myOptions).Create()
       Domoticz.Device(Name="Blokada", Unit=5, TypeName="Switch", Options=myOptions).Create()

     Domoticz.Heartbeat(30)
     Domoticz.Log("Devices created.")


    def onStop(self):
        Domoticz.Log("onStop eQ3 called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect eQ3 called")

    def onMessage(self, Connection, Data, Status, Extra):
        Domoticz.Log("onMessage eQ3 called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        mac = Parameters["Address"]

        if(Command=="Set Level" and Unit==1):
         self.changeTemp(Level,mac)

        if(Unit==4):
         self.changeMode(Level,mac)

        if(Unit==5):
         self.changeLocked(Command,mac)

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect eQ3 called")

    def changeTemp(self,Temp,mac):
        try:
            self.runCommand(' temp '+str(Temp))
        except:
            Domoticz.Log("Error on change tempe to: "+str(Level)+" on mac:"+mac)

    def runCommand(self,param):
        mac = Parameters["Address"]
        cmd = self.plugin_path+'/eq3.exp ' + mac+ ' '+param
        Domoticz.Log(cmd)
        try:
            result = pexpect.run(cmd)
            Domoticz.Log(result.decode("utf-8"))
            time.sleep(2)
            self.refresh()
            return None
        except Exception as e:
            Domoticz.Error("Error durring run command" + str(e))
            return None


    def changeLocked(self,Locked,mac):
        try:

            if(Locked=="On"):
             state = "lock"
             self.updateDevice(5,1,Locked)
            else:
             state = "unlock"
             self.updateDevice(5,0,Locked)

            self.runCommand(state)
        except Exception as e:
            Domoticz.Error("Error during changeLocked" + str(e))
            Domoticz.Log("Error on change lock to: "+str(Level)+" on mac:"+mac)

    def changeMode(self,Level,mac):

        #try:
         if(Level==0):
           state = "off"
         elif(Level==10):
           state="on"
         elif(Level==20):
           state="boost"
         elif(Level==30):
           state="manual"
           if(Devices[4].sValue=="Off"):
            state="temp 5"
         elif(Level==40):
           state="auto"
           if(Devices[4].sValue=="Off"):
            state="temp 5"

         self.runCommand(state)

         if(state != "off"):
          self.updateDevice(4,Level,str(Level))
         else:
          self.updateDevice(4,0,"Off")

          self.refresh()
        #except:
         #  Domoticz.Log("Error on change Mode to: "+str(Level)+" on mac:"+mac)

    def updateDevice(self,Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
     if (Unit in Devices):
     # if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
      Devices[Unit].Update(nValue, str(sValue))
      Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
     return

    def updateBatteryLevel(self,BatteryLevel):
        for Unit in Devices:
         if (Devices[Unit].BatteryLevel != BatteryLevel):
          nValue = Devices[Unit].nValue
          sValue = Devices[Unit].sValue
          Devices[Unit].Update(nValue, str(sValue),BatteryLevel)
          Domoticz.Log("Update Battery "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
         return

    def updateData(self,data):

         if(data==None):
          Domoticz.Log("Brak danych z czujnika")
          return
        # Update Temp from eQ3
         self.updateDevice(1,1,str(data["temperature"]))

       # Update Temp in room
         #Po co jest ten update? co to za urzadzenie?
         #self.updateDevice(2,0,"0")

       # Update Head
         self.updateDevice(3,1,str(data["valve"]))

       # Update Mode
         if(data["mode"]["off"]==True):
          self.updateDevice(4,0,"Off")
         elif(data["mode"]["on"]==True):
          self.updateDevice(4,10,str(10))
         elif(data["mode"]["auto"]==True):
          self.updateDevice(4,40,str(40))
         elif(data["mode"]["manual"]==True):
          self.updateDevice(4,30,str(30))
         elif(data["mode"]["boost"]==True):
          self.updateDevice(4,20,str(20))

       # Update Locked
         if(data["mode"]["locked"]==True):
          self.updateDevice(5,1,"On")
         elif(data["mode"]["locked"]!=True):
          self.updateDevice(5,0,"Off")

       # Update Battery
         if(data["mode"]["low battery"]==True):
          self.updateBatteryLevel(0)
         else:
          self.updateBatteryLevel(255)

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat eQ3 called")
        self.refresh()

    def refresh(self):
        try:
         mac = Parameters["Address"]
         Domoticz.Log(mac)
         Domoticz.Log(self.plugin_path)
         result = pexpect.run(self.plugin_path + '/eq3.exp ' + mac + ' json')
         data = json.loads(result.decode("utf-8"))
         Domoticz.Log(str(data))
         self.updateData(data)
        except Exception as e :
         Domoticz.Error("Error durring run pexpect" + str(e))
         #data = json.load(open('/home/pi/domoticz/plugins/eQ3/test_eq3.json'))
         #self.updateData(data)

global _plugin
_plugin = eQ3Plugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Connection, Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
