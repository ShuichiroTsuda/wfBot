import slackbot.bot
from xml.etree.ElementTree import ElementTree
from urllib import request
import json 
import requests
import re

class SelectPlace:
    def __init__(self,rssurl):
        self.rssurl = rssurl
        self.rss = ElementTree(file = request.urlopen(self.rssurl))
        self.root = self.rss.getroot()

    def pref_list(self):
        lis = []
        for pref in self.root.iter('pref'):
            a = pref.attrib
            lis.append(a['title'])
        return lis
        
    def city_list(self,pref):
        l = []
        a1 = ".//*[@title='" + str(pref) + "']//"
        for city in self.root.iterfind(a1):
            b = city.attrib
            if b['title'] != '警報・注意報':
                l.append(b['title'])
        return l

    def get_text(self,message):
        text = message.body['text']  
        text = text.split(None,1)
        text = text[1]
        return text
    
    def return_data(self,city):
        a1 = ".//*[@title='" + city + "']"
        u = self.root.find(a1)
        info = u.attrib
        url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=" + str(info['id'])
        res = requests.get(url)
        data = json.loads(res.text)
        return data

xml_url = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
a = SelectPlace(xml_url)

@slackbot.bot.respond_to('wf')
def start(message):
    message.send('都道府県名を１つ入力してください (例：pref 京都府)')

@slackbot.bot.respond_to(r'^pref\s北海道')
def pref_h(message):
    message.send('以下の中から選択し,入力してください\n道北\n道東\n道南\n道央\n(例：region 道南)')
    
@slackbot.bot.respond_to(r'^region\s+\S.*')
def region_h(message):
    region = a.get_text(message)
    if region not in ["道北","道南","道東","道央"]:
        message.send("入力が誤っています\n全半角や、スペース、漢字等を確認して、入力し直してください")
    global t
    cities = a.city_list(region)
    t = '以下の中から選択してください(例:city '+ cities[0] +')'
    for c in cities:
        t = t + "\n" + c
    message.send(t)
    global pref
    pref = region

@slackbot.bot.respond_to(r'^pref\s大阪府')
def pref_o(message):
    city = "大阪"
    data = a.return_data(city)
    data = data['forecasts']
    text = ""
    for info in data:
        text = text + info['dateLabel'] + " " + info['telop'] + "\n"
    message.send(text)
    
@slackbot.bot.respond_to(r'^pref\s+\S.*')
def prefecture(message):
    global pref
    pref = a.get_text(message)
    if pref not in ["大阪府","北海道"]:
        if pref not in a.pref_list():
            message.send("入力が誤っています\n全半角、スペース、漢字、都・道・府・県が入っているか、等を確認して、入力し直してください")
        else:    
            global t
            cities = a.city_list(pref)
            t = '以下の中から選択してください(例:city '+ cities[0] +')'
            for c in cities:
                t = t + "\n" + c
            message.send(t)

@slackbot.bot.respond_to(r'^city\s+\S.*')
def cities(message):
    city = a.get_text(message)
    if city in a.city_list(pref):
        data = a.return_data(city)
        data = data['forecasts']
        text = ""
        for info in data:
            text = text + info['dateLabel'] + " " + info['telop'] + "\n"
        message.send(text)
    else:
        message.send("入力が誤っています\n全半角や、スペース、漢字等を確認して入力し直してください")
        
    
    