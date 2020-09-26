import androidhelper
import datetime,time
import uptime
import os
#import wolframalpha

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
        return(f"The time is {datetime.datetime.now().hour} : {datetime.datetime.now().minute}")
    	
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
    
    @staticmethod
    def Wikipedia(q):
        pass

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
        loca=dr.getLastKnownLocation().result.get("passive")
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
        return(f"{hrs}:{min}:{sec}")

    #@staticmethod
   # def 


class ModifySystem:
    ##__Bluetooth settings __##
    @staticmethod
    def OnBluetooth():
        return dr.toggleBluetoothState(True)
    
    @staticmethod
    def OfBluetooth():
        return dr.toggleBluetoothState(False)
    
    @staticmethod
    def MakeDiscoverable():
        return dr.bluetoothMakeDiscoverable(300)
    
    ##__Wifi settings__##
    @staticmethod
    def OnWifi():
        return dr.toggleWifiState(True)
    
    @staticmethod
    def OfWifi():
        return dr.toggleWifiState(False)
    
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
    def OnAirplane():
        dr.toggleAirplaneMode(True)
    
    @staticmethod
    def OfAirplane():
        dr.toggleAirplaneMode(False)
    
    ##__ Volume Related__##    
    @staticmethod
    def SilentMode():
        dr.toggleRingerSilentMode(True)
    
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
    
    @staticmethod
    def CaptureAudio():
        dr.recorderStartMicrophone("/storage/emulated/0/"+str(datetime.datetime.now())+".mp3")
    
    @staticmethod
    def StopRecord():
        try:
            dr.recorderStop()
            return True
        except:
            return False
    
    @staticmethod
    def PlayAudio():
        dr.mediaPlay()



class CallMsg:
    @staticmethod
    def Call(string):
        try:
            #strin is used as we nedd string later on
            strin=DataProcessor.GetInt(string)
            if len(str(strin))==10:
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
                dr.phoneCallNumber(contact_dict.get(caller[0]))
            elif len(caller)==0:
                print("you doesnt have such contact name")
            else:
                dr.dialogCreateAlert("Whom Do You Want To Call","Select whom to call")
                dr.dialogSetItems(caller)       
                dr.dialogShow()
                resp=dr.dialogGetResponse().result.get("item")
                dr.phoneCallNumber(contact_dict.get(caller[resp]))

    @staticmethod
    def Sms(string):
        try:
            #strin is used as we nedd string later on
            strin=DataProcessor.GetInt(string)
            if len(str(strin))==10:
                output.speech_out("what's the message hoe are udl id id tjos")
                dr.smsSend(str(strin),input_.voice_recognizer())
            elif len(str(strin))!=10 and strin !=None:
                print("not a valid number")
            elif strin==None:
                #don't comment it
                # this is to create error so it move to except block
                len(None)
        except:
            caller=DataProcessor.ProcessContact(string)
            if len(caller)==1:
                output.speech_out("what's the message")
                dr.smsSend(contact_dict.get(caller[0]),input_.voice_recognizer())
            elif len(caller)==0:
                print("you doesnt have such contact name")
            else:
                dr.dialogCreateAlert("Whom Do You Want To Call","Select whom to call")
                dr.dialogSetItems(caller)       
                dr.dialogShow()
                resp=dr.dialogGetResponse().result.get("item")
                output.speech_out("what's the message")
                dr.smsSend(contact_dict.get(caller[resp]),input_.voice_recognizer())
    
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





















