import json
import model
import requests
import dialogflowClient
from chatBotConfig import channel_secret, channel_access_token
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, TextSendMessage, MessageEvent, TextMessage
from umsConfig import umsWebApi


handler = WebhookHandler(channel_secret)
linebotApi = LineBotApi(channel_access_token)
dialogflowModel = model.DialogflowModel()
userModel = model.UserModel()


# (1) functions
def model_init_(lineId):
    global dialogflowModel, userModel
    dialogflowModel = model.DialogflowModel()
    userModel = model.UserModel()
    dialogflowModel.lineId = userModel.lineId = lineId


def actionDispatch():
    url = umsWebApi + dialogflowModel.actionName
    
    if (dialogflowModel.actionName in ['create', 'delete', 'update']):
        result = requests.post(url, json=userModel.__dict__)
        
    elif (dialogflowModel.actionName == 'retrieve'):
        result = requests.get(url + '?phone=' + userModel.phone)
        
        
    return result


def replyMessageToUser(replyToken, texts):
    replyMessages = []
    for text in texts:
        replyMessages.append(TextSendMessage(text=text))
    linebotApi.reply_message(replyToken, replyMessages)


# (2) Webhook
def lineWebhook(request):
    # get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return '200 OK'


# (3) Follow Event
@handler.add(FollowEvent)
def handle_follow(event):
    model_init_(event.source.user_id)
    dialogflowModel.lineId = event.source.user_id
    dialogflowModel.eventName = 'welcomeEvent'
    dialogflowClient.eventDispatch(dialogflowModel)
    replyMessageToUser(event.reply_token, dialogflowModel.responses)


# (4) Message Event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    model_init_(event.source.user_id)
    dialogflowModel.queryInput = event.message.text
    dialogflowClient.queryDispatch(dialogflowModel)
    
    if (dialogflowModel.actionName):
        
        if (dialogflowModel.actionName == 'update'):
            dialogflowModel.actionName = 'retrieve'
            userModel.phone = dialogflowModel.parameters['phone']
            result = actionDispatch()
            originalUserData = json.loads(result.text)['userModel']
            newUserData = json.loads(result.text)['userModel']
            
            for key in dialogflowModel.parameters:
                newUserData[key] = dialogflowModel.parameters[key]
                
            dialogflowModel.parameters = newUserData
            dialogflowModel.actionName = 'update'
        
        for key in dialogflowModel.parameters:
            setattr(userModel, key, dialogflowModel.parameters[key])
            
        result = actionDispatch()
        
        if (json.loads(result.text)['result']['code'] == '1'):
            dialogflowModel.parameters = json.loads(result.text)['userModel']
            dialogflowModel.eventName = dialogflowModel.actionName + '_responseEvent'  
            
        else:
            dialogflowModel.eventName = dialogflowModel.actionName + '_failResponseEvent'
            
        if (dialogflowModel.actionName == 'update'):
            dialogflowModel.parameters = originalUserData

        dialogflowClient.eventDispatch(dialogflowModel)

    replyMessageToUser(event.reply_token, dialogflowModel.responses)
    
