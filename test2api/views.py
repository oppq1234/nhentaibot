from django.shortcuts import render
from django.conf import settings
from django.db import models
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
from test2api.models import users
from bs4 import BeautifulSoup
import random
import time
import re
import requests
import numpy as np


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    }

def checklink(num):                             # 回傳網址
        while True:
            num = random.randint(1, 400000)
            origin = "https://nhentai.net/g/" + str(num) + "/"      #轉換成網址
            resp = requests.get(origin, headers = headers)
            if resp.status_code == 200:
                print("號碼：" + str(num))
                print("連線成功")
                return num
            else:
                print("連線代碼：" + str(resp.status_code))
                print("連線錯誤，請重新輸入")

def checkhabbit(habbit, num):
    while True:
        num = random.randint(1, 4500)
        origin = "https://nhentai.net/tag/" + habbit + "/?page=" + str(num)      #轉換成網址
        resp = requests.get(origin, headers = headers)
        if resp.status_code == 200:
            print("號碼：" + str(num))
            print("連線成功")
            return num
        else:
            print("連線代碼：" + str(resp.status_code))
            print("連線錯誤，請重新輸入")

def get_habbit(habbit):
    num = 0
    origin = "https://nhentai.net/tag/" + habbit + "/?page=" + str(checkhabbit(habbit, num))
    soup = requests.get(origin, headers = headers)
    tt = soup.find_all("a", class_ = "cover", limit = 25)            # 在此類型中隨機挑選本號

    temp_num = []

    for tts in tt:
        temp_num.append(tts.get("href"))

    return temp_num[random.randint(0, 24)]

def set_habbit(num, user_id):
    tag_total = []
    tag_total.clear()
    origin = "https://nhentai.net/g/" + str(num)
    resp = requests.get(origin, headers = headers)

    if users.objects.filter(uid = user_id).exists() == True:
        userdata = users.objects.get(uid = user_id)
        if userdata.habbit != '':
            tag_total = re.split(" |\n", userdata.habbit)          # ???多一個元素
            tag_total.pop()
            ttmp = []
            for i in range(0, len(tag_total), 2):
                pp = []
                pp.append(tag_total[i])
                pp.append(int(tag_total[i + 1]))
                ttmp.append(pp)
            tag_total = ttmp
        
    soup = BeautifulSoup(resp.text, 'html.parser')
    tags = soup.find_all('span', class_ = "name")                    # 記錄當前本子標籤

    for tag in tags:
        tag_title = []
        temp = tag_total
        # print(tag.string)

        if tag.string == "doujinshi" or tag.string == "chinese" or tag.string == "translated" or tag.string == "doujinshi" or tag.string == "japanese" or tag.string == "english" or tag.string == "manga":
            continue

        if tag.string.isdigit() == True:
            continue

        tag.string = tag.string.replace(" ", "-")

        if tag_total:
            temp.sort(key = lambda x:x[0] != tag.string)
        try:
            if temp and tag.string == temp[0][0]:
                temp[0][1] = temp[0][1] + 1
                tag_total = temp
            else:
                if len(tag_total) > 110:
                    tag_total.pop()
                tag_title.append(tag.string)
                tag_title.append(1)
                tag_total.append(tag_title)
        except:
            print("error")
            tag_total.append(np.nan)
    # print(*tag_total, sep = "\n")
    tag_total = sorted(tag_total, key = lambda s: s[1], reverse = True)

    tag_total.pop()
    result = []
    for i in range(len(tag_total)):
        result.extend(tag_total[i])
    print(result)
    tag_total = result
    userdata.habbit = ''
    for i in range(0, len(tag_total), 2):
        userdata.habbit = userdata.habbit + tag_total[i] + " " + str(tag_total[i + 1]) + "\n"
    # userdata.habbit = "\n".join(tag_total) # 這邊改
    userdata.save()

    time.sleep(1)
    print("-----------------------------------------")

def set_dislike(num, user_id):
    tag_total = []
    tag_total.clear()
    origin = "https://nhentai.net/g/" + str(num)
    resp = requests.get(origin, headers = headers)
    if users.objects.filter(uid = user_id).exists() == True:
        userdata = users.objects.get(uid = user_id)
        if userdata.habbit != '':
            tag_total = re.split(" |\n", userdata.habbit)          # ???多一個元素
            tag_total.pop()
            ttmp = []
            for i in range(0, len(tag_total), 2):
                pp = []
                pp.append(tag_total[i])
                pp.append(int(tag_total[i + 1]))
                ttmp.append(pp)
            tag_total = ttmp
        
    soup = BeautifulSoup(resp.text, 'html.parser')
    tags = soup.find_all('span', class_ = "name")                    # 記錄當前本子標籤
    for tag in tags:
        tag_title = []
        temp = tag_total    

        if tag.string == "doujinshi" or tag.string == "chinese" or tag.string == "translated" or tag.string == "doujinshi" or tag.string == "japanese" or tag.string == "english" or tag.string == "manga":
            continue

        if tag.string.isdigit() == True:
            continue

        tag.string = tag.string.replace(" ", "-")

        if tag_total:
            temp.sort(key = lambda x:x[0] != tag.string)
        try:
            if temp and tag.string == temp[0][0]:
                temp[0][1] = temp[0][1] - 1
                tag_total = temp
            else:
                if len(tag_total) > 110:
                    tag_total.pop()
                tag_title.append(tag.string)
                tag_title.append(-1)
                tag_total.append(tag_title)
        except:
            print("error")
            tag_total.append(np.nan)
    # print(*tag_total, sep = "\n")
    tag_total = sorted(tag_total, key = lambda s: s[1], reverse = True)

    tag_total.pop()
    result = []
    for i in range(len(tag_total)):
        result.extend(tag_total[i])
    tag_total = result
    for i in range(0, len(tag_total), 2):
        userdata.habbit = userdata.habbit + tag_total[i] + " " + str(tag_total[i + 1]) + "\n"
    # userdata.habbit = "\n".join(tag_total) # 這邊改
    userdata.save()

    time.sleep(1)
    print("-----------------------------------------")

def sendConfirm(event):  #確認樣板
    try:
        num = 0
        
        num = checklink(num)
        # line_bot_api.reply_message(event.reply_token,TextSendMessage(text='f'))
        message = [TextSendMessage(text = 'https://nhentai.net/g/' + str(num)), 
        TemplateSendMessage(
            alt_text= "取代",
            template=ConfirmTemplate(
                text= '您喜歡這本嗎？',
                actions=[
                    MessageTemplateAction(  #按鈕選項
                        label='這本不錯',
                        text= '@yes ' + str(num)
                    ),
                    MessageTemplateAction(
                        label='幹這本好噁',
                        text= '@no ' + str(num)
                    )
                ]
            )
        )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def habbitConfirm(event, user_id):  #確認樣板
    try:
        
        if users.objects.filter(uid = user_id).exists() == True:
            userdata = users.objects.get(uid = user_id)
        if userdata.habbit != '':
            tag_total = re.split(" |\n", userdata.habbit)          # ???多一個元素
            tag_total.pop()
            ttmp = []
            for i in range(0, len(tag_total), 2):
                pp = []
                pp.append(tag_total[i])
                pp.append(int(tag_total[i + 1]))
                ttmp.append(pp)
            tag_total = ttmp
        seed = random.randint(1, len(tag_total) / 5)

        habbit = tag_total[seed][0]
        
        num = get_habbit(habbit)
        # line_bot_api.reply_message(event.reply_token,TextSendMessage(text='f'))
        message = [TextSendMessage(text = 'https://nhentai.net/g/' + str(num)), 
        TemplateSendMessage(
            alt_text= "取代",
            template=ConfirmTemplate(
                text= '您喜歡這本嗎？',
                actions=[
                    MessageTemplateAction(  #按鈕選項
                        label='這本不錯',
                        text= '@yes ' + str(num)
                    ),
                    MessageTemplateAction(
                        label='幹這本好噁',
                        text= '@no ' + str(num)
                    )
                ]
            )
        )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:            # 依序處理所有事件
            if isinstance(event, MessageEvent):     # 是否為訊息事件
                user_id = event.source.user_id
                try:
                    if users.objects.filter(uid = user_id).exists() == False:
                        unit = users.objects.create(uid = user_id)
                        unit.save()
                except:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text ='error'))
                
                text1 = event.message.text
                # text1 == 'car' or text1 == '車' or text1 == 'Car'
                if text1.find("car") != -1:
                    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text = 'https://nhentai.net/g/' + str(random.randint(1, 324000))))
                    sendConfirm(event)
                elif text1.find("habbitcar") != -1:                 
                    habbitConfirm(event, user_id)
                elif text1.find("@yes") != -1:                          
                    number = ''.join([x for x in text1 if x.isdigit()])         # 把text1裡的數字抓出來
                    
                    set_habbit(number, user_id)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text ='好色喔，竟然喜歡這種本，我記下來了欸嘿'))
                elif text1.find("@no") != -1:           # 待補
                    number = ''.join([x for x in text1 if x.isdigit()])         # 把text1裡的數字抓出來
                    set_dislike(number, user_id)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text ='抱歉讓你傷到眼了，以後應該不會再看到這種本了，大概'))
                           
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
# Create your views here.