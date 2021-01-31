import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from model import UserModel, UserResponse

userModel = UserModel()
userResponse = UserResponse()

cred = credentials.Certificate('firebaseKey.json')
initialize_app(cred)
db = firestore.client()
users_ref = db.collection('users')

def create(request):
    request_json = request.get_json()
    id = request_json['phone']

    userModel = UserModel(**request_json)
    userResponse.userModel = userModel.__dict__

    user = users_ref.document(id).get().to_dict()

    if(user == None):
        users_ref.document(id).set(userModel.__dict__)
        userResponse.result = {
            "code": "1",
            "title": "註冊完成",
        }
    else:
        userResponse.result = {
            "code": "-1",
            "title": "重複註冊",
            "description": "本手機("+str(id)+")已由他人註冊"
        }
    
    return userResponse.__dict__

