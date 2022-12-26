from transitions import Machine
from flask import Flask
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,QuickReply,QuickReplyButton,MessageAction
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DATE
from env import *
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from transitions.extensions import GraphMachine
from geopy.geocoders import Nominatim
import os


SQLALCHEMY_DATABASE_URL = database_uri

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # inherit from this class to create ORM models
session = sessionmaker(engine)
db = session()

class elevator(Base):
    __tablename__ = 'elevators'
    sid = Column(Integer,primary_key = True)
    name = Column(String(200),nullable = False)
    date = Column(DATE)
    live = Column(Boolean)
    
    def __init__(self,name,date):
        self.name = name,
        self.date = date,
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =  database_uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db=SQLAlchemy(app)



class bot(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['init', 'tutorial', 'elevator', 'playground','help_elevator','Map','getDB','newDB','deleteDB','News','Weather']
    msg = ""
    target = 0
    Region = ""
    quickply = 0
    reply = ""
    



    def __init__(self, name):
        
        self.name = name
       
        self.feature = ""
        
        self.willImg = 0
        
        self.statistics = {} 
        
        self.msg_array = []

        self.machine = Machine(model=self, states=bot.states, initial='init')
        
        self.machine.add_transition('help','init','tutorial')

        self.machine.add_transition('news',['init','tutorial','News'],'News')
        
        self.machine.add_transition('weather',['init','tutorial'],'Weather',before = 'showWeatherStatus')
        
        self.machine.add_transition('Region','Weather','=',before = 'changeRegion')
        
        self.machine.add_transition('wx8','Weather','=',conditions= 'hasRegion',after ='getWx')
        
        self.machine.add_transition('maxT','Weather','=',conditions= 'hasRegion',after ='getMaxT')
       
        self.machine.add_transition('minT','Weather','=',conditions= 'hasRegion',after ='getMinT') 
        
        self.machine.add_transition('ci','Weather','=',conditions= 'hasRegion',after ='getCi')
        
        self.machine.add_transition('pop','Weather','=',conditions= 'hasRegion',after ='getPop')  
        # wx8    # 天氣現象
# maxtT  # 最高溫
# mintT # 最低溫
# ci   # 舒適度
# pop  # 降雨機率
        
        self.machine.add_transition('play',['init','tutorial'],'playground',before = 'random_number')
        
        self.machine.add_transition('map',['init','tutorial'],'Map',after = 'map_info')
        
        self.machine.add_transition('position','Map','=', after = "positionInfo")
        
        self.machine.add_transition('positionInfo','Map','=',conditions='hasfeature',after = 'posImg')
        
        self.machine.add_transition('guess','playground','=',before = 'guess')
        
        self.machine.add_transition('exit','*','init')
        
        self.machine.add_transition('refrigerator',['init','tutorial','help_elevator'],'elevator')
        
        self.machine.add_transition('db',['elevator','help_elevator','newDB','deleteDB'],'getDB',after = 'printDB')
        
        self.machine.add_transition('new',['elevator','help_elevator','getDB','deleteDB'],'newDB',after = 'newItemDB')
        
        self.machine.add_transition('delete',['elevator','help_elevator','newDB','getDB'],'deleteDB',after = 'deleteItemDB')
        
        self.machine.add_transition('db','getDB','=',before = 'printDB')
        
        self.machine.add_transition('new','newDB','=',before = 'newItemDB')
        
        self.machine.add_transition('delete','deleteDB','=',before = 'deleteItemDB')
        
        self.machine.add_transition('help', ['elevator','getDB','newDB','deleteDB'],'help_elevator')
               
        self.machine.on_enter_tutorial(self.print_info) 
        
        self.machine.on_enter_elevator(self.print_elevator)
        
        self.machine.on_enter_init(self.in_init)

        self.machine.on_enter_News(self.news)
        
        self.machine.on_enter_help_elevator(self.help_in_elevator)

        
    def in_init(self):
        self.msg = "hi it is robot ! You can use help command to get info"

    def news(self):
        response = requests.get("https://www.bbc.com/news")
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find_all("li",  class_="gel-layout__item gs-o-faux-block-link gs-u-mb+ gel-1/2@m gs-u-float-left@m gs-u-clear-left@m gs-u-float-none@xxl")
        self.msg = "From BBC Most read news top 5 : \n"
        j = 1
        for i in result:
          try:
              self.msg += str(j) + " : " + str(i.find('span').text[1:-1]) + "\n"
              self.msg += "https://www.bbc.com" + str(i.find('a')['href']) + "\n"
              j+=1
          except:
              print('error')

    def getWx(self):
        for i in range(3):
            self.msg += self.statistics[self.Region]['Wx']['time'][i]['startTime'] + " ~ "
            self.msg += self.statistics[self.Region]['Wx']['time'][i]['endTime'] + "\n" 
            self.msg += self.statistics[self.Region]['Wx']['time'][i]['parameter']['parameterName'] + "\n\n" 
       
        
    def getMaxT(self):
       for i in range(3):
            self.msg += self.statistics[self.Region]['MaxT']['time'][i]['startTime'] + " ~ "
            self.msg += self.statistics[self.Region]['MaxT']['time'][i]['endTime'] + "\n" 
            self.msg += self.statistics[self.Region]['MaxT']['time'][i]['parameter']['parameterName'] + " C \n\n" 
        
    def getMinT(self):
        for i in range(3):
            self.msg += self.statistics[self.Region]['MinT']['time'][i]['startTime'] + " ~ "
            self.msg += self.statistics[self.Region]['MinT']['time'][i]['endTime'] + "\n" 
            self.msg += self.statistics[self.Region]['MinT']['time'][i]['parameter']['parameterName'] + " C \n\n" 
         
    def getCi(self):
       for i in range(3):
            self.msg += self.statistics[self.Region]['CI']['time'][i]['startTime'] + " ~ "
            self.msg += self.statistics[self.Region]['CI']['time'][i]['endTime'] + "\n" 
            self.msg += self.statistics[self.Region]['CI']['time'][i]['parameter']['parameterName'] + "\n\n" 
          
    def getPop(self):
       for i in range(3):
            self.msg += self.statistics[self.Region]['PoP']['time'][i]['startTime'] + " ~ "
            self.msg += self.statistics[self.Region]['PoP']['time'][i]['endTime'] + "\n" 
            self.msg += self.statistics[self.Region]['PoP']['time'][i]['parameter']['parameterName'] + " % \n\n" 
          

        
    def print_info(self):
        self.msg = \
        ''' 
welcome !
This is useful help!
If you want to play guess number game, you can type "play"  
If you want to check weather info, you can type "weather"  
If you want to check the items in you refrigerator, you can type "refrigerator"  
If you want to catch up the news, you can type "news"  
If you want to know the certain address info, you can type "map"
        '''
        
    def random_number(self):
        self.target = int(random.random() * 100)
        self.msg = " Let's guess ! \n Please use 'guess number' to guess ! "
        
    def guess(self,number):
        number = int(number)
        if(number > self.target):
            self.msg = "lower"
        elif (number < self.target) :
            self.msg = "higher"
        else:
            self.msg ="bingo ! \n And I will change target number !"
            self.target = int(random.random() * 100)
            
    def print_elevator(self):
        self.msg = ''' 
            This is your refrigerator!! \n
            You can use [ help ] command to get help
            '''
    def help_in_elevator(self):
        self.msg = \
        '''This is your help:
        (1) db : get your items in your refrigerator
        (2) new : put items in your refrigerator
        \t usage : new itemName date 
        \t example : new water 12/31
        (3) delete : delete items in your refrigerator
        \t usage : delete itemName
        \t example : delete water
        '''
        
    def printDB(self):
        items = db.query(elevator)
        msg="" 
        for item in items:
            msg+=f"{item.name}, {item.date} \n"
        self.msg = msg
        
    def newItemDB(self,name,date):
        if int(date.split('/')[0]) >= 12:
            date = datetime.date(2022,int(date.split('/')[0]), int(date.split('/')[1]))  #data -> 12/04
        else:
            date = datetime.date(2023,int(date.split('/')[0]), int(date.split('/')[1]))  #data -> 12/04
        item = elevator(name,date)
        db.add(item)
        db.commit()
        self.msg = "add " + str(name)
        
    def positionInfo(self,event):
        geolocator = Nominatim(user_agent="geoapiExercises")
        print(str(event.message.latitude) + "," + str(event.message.longitude))
        location = geolocator.reverse( str(event.message.latitude) + "," + str(event.message.longitude)  )
        print(location.raw['address'])
        list_feature = ['emergency', 'historic', 'military', 'natural', 'landuse', 'place', 'railway', 'man_made', 'aerialway', 'boundary', 'amenity', 'aeroway', 'club', 'craft', 'leisure', 'office', 'mountain_pass', 'shop', 'tourism', 'bridge', 'tunnel', 'waterway']
        self.msg = "position : " +  str(event.message.latitude) + "," + str(event.message.longitude) + "\n"
        for i in list_feature:
            if i in location.raw['address'] :
                self.feature = str(location.raw['address'][i])
                self.msg += "Target Name : " + str(location.raw['address'][i]) + "\n"
                break
            else :
                self.feature  = "" 
        if 'house_number' in  location.raw['address'] : 
            self.msg += "Address : " + str(location.raw['address']['country']) + str(location.raw['address']['city']) + str(location.raw['address']['road']) + str(location.raw['address']['house_number'])
        else :
            self.msg += "Address : " + str(location.raw['address']['country']) + str(location.raw['address']['city']) + str(location.raw['address']['road'])

        
    def deleteItemDB(self,name):
        db.query(elevator).filter(elevator.name == name).delete()
        db.commit()
        self.msg = "delete " + str(name) +" success"
        
    def map_info(self):
        self.msg = "you can use position to get address and feature ! \n if you already get info, you can get special info from command positionInfo"
        self.quickply = 1
        self.reply = QuickReply(
            items=[
                QuickReplyButton(action = MessageAction(label="Info", text="positionInfo")
                )])
    
    def weatherInfo(self):
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-0B96D55D-CC71-4632-ACA1-1AC1E742361F'
        data = requests.get(url)   # 取得 JSON 檔案的內容為文字
        data_json = data.json()    # 轉換成 JSON 格式
        for i in data_json['records']['location']:
            cityname = i['locationName']
            for j in i['weatherElement']:
                weather = j['elementName']

                if cityname not in self.statistics:
                    self.statistics[cityname] = {weather: j}

                if weather not in self.statistics[cityname]:
                    self.statistics[cityname][weather] = j    
                    
    def showWeatherStatus(self):
        if(self.statistics == {}):
            self.weatherInfo()
            self.msg = "please use Region to reset region before you go down"
            self.Region = ""
        
    def hasRegion(self):
        if(self.Region == ""):
            self.msg = "you dont set region, please use Region to reset region before you go down "
            return False
        else:
            return True
        
    def hasfeature(self):
        if(self.feature == ""):
            self.msg = "this places do not have feature"
            return False
        else:
            return True
        
    def changeRegion(self,Region):
        if self.statistics.get(Region) == None:
            self.msg = "do not have this " + Region + " please use Region to reset region before you go down"
            self.Region = ""
        else:
            self.Region = Region
            self.msg = " set Region success \n use wx8 to get weather \n use maxT to get highest Temp \n use minT to get lowest Temp \n use ci to get comfort info \n use pop to get the property of rain"
    def posImg(self):
        self.willImg = 1
        url = 'https://www.google.com/search?q=' + self.feature +'&rlz=1C2CAFB_enTW617TW617&source=lnms&tbm=isch&sa=X&ved=0ahUKEwictOnTmYDcAhXGV7wKHX-OApwQ_AUICigB&biw=1128&bih=960'
        photolimit = 5
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url,headers = headers) #使用header避免訪問受到限制
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('img')
        folder_path ='./static/'
        if (os.path.exists(folder_path) == False): #判斷資料夾是否存在
            os.makedirs(folder_path) #Create folder
        else :
            for file_name in os.listdir("./static/"):
                if(file_name == "preview.jpg") :
                    continue
                elif(file_name == 'video.mp4'):
                    continue
                file = "./static/" + file_name #### will need to be fix
                if os.path.isfile(file) :
                    print('Deleting file:', file)
                    os.remove(file)
        for index , item in enumerate (items):
            if (item and index < photolimit ):
                print(item)
            try:
                html = requests.get(item.get('src')) # use 'get' to get photo link path , requests = send request
                img_name = folder_path + str(index + 1) + '.png'
                with open(img_name,'wb') as file: #以byte的形式將圖片數據寫入
                    file.write(html.content)
                    file.flush()
                file.close() #close file    
            except:
                print("error")
        count = 0
        for i in range(5):
            if os.path.isfile("./static/" + str(i+1) + ".png"):
                self.msg_array.append(ImageSendMessage(original_content_url = ngrok_url + "/static/" + str(i+1) + ".png", preview_image_url = ngrok_url + "/static/" + str(i+1)  + ".png"))
                count +=1
                if count == 3:
                    break

    
        
        
batman = bot("Batman")
# in cases where auto transitions should be visible
#machine = GraphMachine(model=bot("test"), show_auto_transitions=True)
#machine.get_graph().draw('my_state_diagram.png', prog='dot')
# draw the whole graph ...
#m.get_graph().draw('my_state_diagram.png', prog='dot')
