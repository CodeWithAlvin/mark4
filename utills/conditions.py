try:
    import functions
except:
    import utills.functions as functions
try:
    from data import query , answer
except:
    from utills.data import query , answer
from random import choice
#global vars
appkey=[i.lower() for i,j in functions.dr.getLaunchableApplications().result.items()]
def Process(cmd):
    if any(i in cmd for i in query.hay):
        return(choice(answer.hay))
    elif any(i in cmd for i in query.hey):
        return(choice(answer.hey))
    elif any(i in cmd for i in query.wayd):
        return(choice(answer.wayd))
    elif any(i in cmd for i in query.wcyd):
        return(choice(answer.wcyd))
    elif any(i in cmd for i in query.intro):
        return(choice(answer.intro))
    elif any(i in cmd for i in query.tyme):
        return(functions.TimeDate.CurrentTime())
    elif any(i in cmd for i in query.date):
        return(functions.TimeDate.CurrentDate())
    elif any(i in cmd for i in query.audio):
        return(functions.Media.CaptureAudio())
    elif any(i in cmd for i in query.video):
        return(functions.Media.CaptureVideo())
    elif any(i in cmd for i in query.scan):
        return(functions.Media.ScanBarcode())
    elif all(i in cmd for i in ["stop","recording"]):
        return(functions.Media.StopRecord())
    elif "uptime" in cmd or "up time" in cmd:
        return(f"it's {functions.SystemStats.Uptime()}")
    elif "battery" in cmd:
        level=functions.SystemStats.BatteryInfo().get("level")
        temperature=functions.SystemStats.BatteryInfo().get("temperature")/10
        return(f"sir ,battery level is {level} % and temperature is {temperature} °C")
    elif any(i in cmd for i in query.location):
        loc=functions.SystemStats.Location()
        return (f"it's {loc[0]}° latitudinal and {loc[1]}° longitudinal")
    elif all(i in cmd for i in ["on","bluetooth"]):
        return(functions.ModifySystem.ToggleBluetooth(True))
    elif all(i in cmd for i in ["off","bluetooth"]):
        return(functions.ModifySystem.ToggleBluetooth(False))
    elif all(i in cmd for i in ["Discover","bluetooth"]):
        return(functions.ModifySystem.ToggleBluetooth())
    elif all(i in cmd for i in ["on","wi-fi"]):
        return(functions.ModifySystem.ToggleWifi(True))
    elif all(i in cmd for i in ["of","wi-fi"]):
        return(functions.ModifySystem.ToggleWifi(False))
    elif all(i in cmd for i in ["close","wi-fi"]):
        return(functions.ModifySystem.CloseConn())
    elif all(i in cmd for i in ["reconnect","wi-fi"]):
        return(functions.ModifySystem.Reconnect())
    elif all(i in cmd for i in ["info","wi-fi"]):
        return(functions.ModifySystem.GetConnId())
    elif all(i in cmd for i in ["on","airplane"]):
        return(functions.ModifySystem.ToggleAirplane(True))
    elif all(i in cmd for i in ["of","airplane"]):
        return(functions.ModifySystem.ToggleAirplane(False))
    elif all(i in cmd for i in ["off","silent","mode"]):
        functions.ModifySystem.SilentMode(False)
    elif all(i in cmd for i in ["silent","mode"]):
        functions.ModifySystem.SilentMode(True)
    elif all(i in cmd for i in ["max","volume"]):
        functions.ModifySystem.MaxVolume()
    elif all(i in cmd for i in ["set","volume"]):
        functions.ModifySystem.SetVolume(cmd)
    elif "call" in cmd:
        return(functions.CallMsg.Call(cmd))
    elif "message" in cmd:
        return(functions.CallMsg.Sms(cmd))
    elif  any(apk_name in cmd for apk_name in appkey):
        functions.AppWeb.OpenApp(cmd)
    elif any(i in cmd for i in ["open","search"]):
        functions.AppWeb.OpenWeb(cmd)
    elif "wolf" in cmd:
        return functions.Queries.Wolframalpha(cmd)
    else :
        None









