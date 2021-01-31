import os
from firebase_admin import credentials, firestore, initialize_app
import requests
import json
from model import UserModel,UserResponse

userModel = UserModel()
userResponse = UserResponse()

cred = credentials.Certificate('firebaseKey.json')
initialize_app(cred)
db = firestore.client()
users_ref = db.collection('users')


def retrieve(request):
    
    request_args = request.args
    if(request.args and 'phone' in request.args):
        id = request.args.get('phone')
        user = users_ref.document(id).get().to_dict()
        if(user != None):
            userResponse.userModel = user
            userResponse.result ={
                    "code":"1",
                    "title":"查詢完成",
                }
        else:
            userResponse.userModel = {}
            userResponse.result ={
                    "code":"-1",
                    "title":"無相關資料",
                    "description":"本手機("+str(id)+")尚未由他人註冊"
                }
    else:
        userResponse.userModel = [doc.to_dict() for doc in users_ref.stream()]
        userResponse.result ={
                    "code":"1",
                    "title":"人員列表",
                }
    return userResponse.__dict__
