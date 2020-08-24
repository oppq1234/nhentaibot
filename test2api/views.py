from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


def sendConfirm(event):  #確認樣板
    try:
        num = random.randint(1, 324000)
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
                text1 = event.message.text
                if text1 == 'car' or text1 == '車' or text1 == 'Car':
                    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text = 'https://nhentai.net/g/' + str(random.randint(1, 324000))))
                    sendConfirm(event)          

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
# Create your views here.