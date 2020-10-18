import androidhelper
import datetime,time
import uptime
import os
import wolframalpha

#global variables
dr=androidhelper.Android()
contact_dict={}


#classes 

#class to take input
class input_:
    @staticmethod
    def voice_recognizer():
        """
        Takes input as voice command
        using google voice recognizer
        """
        while dr.ttsIsSpeaking().result or dr.mediaIsPlaying().result:
            time.sleep(1)
        return dr.recognizeSpeech().result
    	
    	
    @staticmethod
    def text_input():
        """
        Takes input as text 
        """
        return input(">>>")
    
#class to give output
class output:
    @staticmethod
    def speech_out(x):
        """
        return speech output
        arg x = anything valid
        """
        dr.ttsSpeak(x)
    	
    @staticmethod
    def text_out(x):
        """
        return text output
        arg x : x is any valid input
        """
        print(x)
    
#class for time & date related things
class TimeDate:
    @staticmethod
    def CurrentTime():
        return(f"Sir , The time is {datetime.datetime.now().hour} : {datetime.datetime.now().minute}")
    	
    @staticmethod
    def CurrentDate():
        return(f"sir! today's date is {time.strftime('%A %e')} on {time.strftime('%B,%Y')}")
    	
#class to connect with sql database
class Database: 
    @staticmethod
    def Base():
        database="/storage/emulated/0/python/Assistants/Mark4/utills/Jarvis.db"
        conn=sqlite.connect(database)
        cur=conn.cursor()
    
    @staticmethod
    def DataChanger(query):
        Database.Base()
        try:
            cur.exexute(query)
            conn.commit()
            return("command sucessfully executed")
        except error as e:
            print(e)
    
    @staticmethod
    def DataFetcher(query):
        Database.Base()
        try:
            cur.exexute(query)
            return cur.fetchall()
        except error as e:
            print(e)

#class for Queries
class Queries:
    @staticmethod
    def Wolframalpha(q):
        key="T7JEE3-78JVW6PG6Q" 
        client=wolframalpha.Client(key)
        res=client.query(q)
        answer=next(res.results).text
        return(answer)
    

class AppWeb:
    @staticmethod
    def OpenApp(query):
        apk_dict=dr.getLaunchableApplications().result
        alphalower = {k.lower(): v for k, v in apk_dict.items()}           
        app_name=[k for k in alphalower.keys() if k in query]       	
        try:           
            dr.launch(alphalower.get(app_name[0]))
            inp=input("enter to continue\n")
        except:
            None
    
    @staticmethod
    def OpenWeb(query):
        try:
            query=query.replace("open","")
            query=query.replace("search","")
        except:
            None
        dr.search(query)    	 		

class SystemStats:
    @staticmethod
    def BatteryInfo():
        dr.batteryStartMonitoring()
        data=dr.readBatteryData().result        
        dr.batteryStopMonitoring()
        return data
        
    @staticmethod
    def Location():
        dr.startLocating()
        loca=dr.getLastKnownLocation().result.get("gps")
        lati=loca.get("latitude")
        longi=loca.get("longitude")
        return(lati,longi)

    @staticmethod
    def Uptime():
        raw=int(uptime.uptime())
        Tmin=raw//60
        sec=raw%60
        hrs=Tmin//60
        min=Tmin%60
        return(f"{hrs} hours :{min} minutes :{sec} seconds")


class ModifySystem:
    ##__Bluetooth settings __##
    @staticmethod
    def ToggleBluetooth(arg):
        return dr.toggleBluetoothState(arg) 
        
    @staticmethod
    def MakeDiscoverable():
        return dr.bluetoothMakeDiscoverable(300)
    
    ##__Wifi settings__##
    @staticmethod
    def ToggleWifi(arg):
        return dr.toggleWifiState(arg)
        
    @staticmethod 
    def CloseConn():
        return dr.wifiDisconnect()
    
    @staticmethod
    def Reconnect():
        return dr.wifiReconnect()
    
    @staticmethod
    def GetConnId():
        return dr.wifiGetConnectionInfo()
    
    @staticmethod
    def GetResult():
        dr.wifiStartScan()
        return dr.wifiGetScanResults().result
    
    ##__Airplane Mode__##
    @staticmethod
    def ToggleAirplane(arg):
        return(dr.toggleAirplaneMode(arg))
      
    ##__ Volume Related__##    
    @staticmethod
    def SilentMode(arg):
        dr.toggleRingerSilentMode(arg)
    
    @staticmethod
    def MaxVolume():
        dr.setRingerVolume(dr.getMaxRingerVolume().result)
        dr.setMediaVolume(dr.getMaxMediaVolume().result)
    
    @staticmethod
    def SetVolume(string):
        x=DataProcessor.GetInt(string)
        dr.setRingerVolume(x)
        dr.setMediaVolume(x)

class Media:
    @staticmethod
    def CapturePicture():
        return(dr.cameraCapturePicture("/storage/emulated/0/"+str(datetime.datetime.now())+".jpg").result.get("takePicture"))
    
    @staticmethod
    def ScanBarcode():
        return dr.scanBarcode().result.get("extras").get("SCAN_RESULT")
    
    @staticmethod
    def CaptureVideo():
        dr.recorderStartVideo("/storage/emulated/0/"+str(datetime.datetime.now())+".mp4",0,400)
        return ("started")
    @staticmethod
    def CaptureAudio():
        dr.recorderStartMicrophone("/storage/emulated/0/"+str(datetime.datetime.now())+".mp3")
        return ("started")
    @staticmethod
    def StopRecord():
        try:
            dr.recorderStop()
            return("stopped")
        except:
            return("there is no recordings to stop")
    

class CallMsg:
    @staticmethod
    def Call(string):
        try:
            #strin is used as we nedd string later on
            strin=DataProcessor.GetInt(string)
            if len(str(strin))==10:
                output.speech_out(f"calling {strin}")
                dr.phoneCallNumber(str(strin))
            elif len(str(strin))!=10 and strin !=None:
                print("not a valid number")
            elif strin==None:
                #don't comment it
                # this is to create error so it move to except block
                len(None)
        except:
            caller=DataProcessor.ProcessContact(string)
            if len(caller)==1:
                output.speech_out(f"calling {caller[0]}")
                dr.phoneCallNumber(contact_dict.get(caller[0]))
            elif len(caller)==0:
                print("you doesnt have such contact name")
            else:
                dr.dialogCreateAlert("Whom Do You Want To Call","Select whom to call")
                dr.dialogSetItems(caller)       
                dr.dialogShow()
                resp=dr.dialogGetResponse().result.get("item")
                output.speech_out(f"calling {caller[resp]}")
                dr.phoneCallNumber(contact_dict.get(caller[resp]))

    @staticmethod
    def Sms(string):
        contact=None
        try:
            #strin is used as we nedd string later on
            strin=DataProcessor.GetInt(string)
            if len(str(strin))==10:
                contact=strin
            elif len(str(strin))!=10 and strin !=None:
                print("not a valid number")
            elif strin==None:
                #don't comment it
                # this is to create error so it move to except block
                len(None)
        except:
            caller=DataProcessor.ProcessContact(string)
            if len(caller)==1:
                contact=contact_dict.get(caller[0])
            elif len(caller)==0:
                print("you doesnt have such contact name")
            else:
                dr.dialogCreateAlert("Whom Do You Want To Message","Select whom to msg")
                dr.dialogSetItems(caller)       
                dr.dialogShow()
                resp=dr.dialogGetResponse().result.get("item")
                contact=contact_dict.get(caller[resp])
        finally:
            if contact!=None:
                output.speech_out("what's the message")
                while True:
                    msg=input_.voice_recognizer()
                    output.speech_out("wanna send it")
                    conf=input_.voice_recognizer()
                    if any(i in conf for i in ["exit","stop","cancel","no"]):
                        output.speech_out("No problem nothing done")
                        break
                    else:                        
                        dr.smsSend(contact,msg)
                        output.speech_out("message sended")
                        break
    
    @staticmethod
    def SendMail(to,content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        dr.dialogCreatePassword("Password", "enter password")
        dr.dialogSetPositiveButtonText("Submit")
        dr.dialogShow()
        server.login('sainialvin@gmail.com',dr.dialogGetResponse().result.get("value"))
        server.sendmail('sainialvin@gmail.com', to, content)
        server.close()


class OuterEnviron:
    def Weather():
        pass



        

class DataProcessor:
    @staticmethod
    def ContactData():
        global contact_dict
        cdata = dr.queryContent('content://com.android.contacts/data/phones',['display_name','data1'],None,None,None).result
        for i in range(len(cdata)):
            contact_dict[cdata[i].get("display_name").lower()]=cdata[i].get("data1")
    
    @staticmethod
    def GetInt(string):
        lis=string.split()     
        for item in lis[0:len(lis)]:
            if item.isdigit():
                value=int(item)
                return(value)
    
    @staticmethod
    def ProcessContact(phrase):
        DataProcessor.ContactData()
        contact=contact_dict
        names=contact.keys()
        phrase=phrase.split(" ")
        lis=[]
        for word in phrase:
            for name in names:
                if word in name:
                    lis.append(name)
        return lis










