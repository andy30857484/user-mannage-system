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

def update(request):
    
    request_json = request.get_json()
    id = request_json['phone']
    
    userModel = UserModel(**request_json)
    userResponse.userModel = request_json

    user = users_ref.document(id).get().to_dict()
    if(user != None):
            users_ref.document(id).set(userModel.__dict__,merge=True)
            userResponse.result ={
                    "code":"1",
                    "title":"修改完成",
                }
    else:
        userResponse.userModel = {}
        userResponse.result ={
                "code":"-1",
                "title":"修改失敗",
                "description":"本手機("+str(id)+")尚未由他人註冊"
            }
    
    return userResponse.__dict__
