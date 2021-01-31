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

def delete(request):
    
    request_json = request.get_json()
    id = request_json['phone']
    
    userResponse.userModel = {}
    
    user = users_ref.document(id).get().to_dict()
    
    if(user != None):
        users_ref.document(id).delete()
        userResponse.result ={
                "code":"1",
                "title":"退出完成",
            }
    else:
        userResponse.result ={
                "code":"-1",
                "title":"無相關資料",
            }
    return userResponse.__dict__
