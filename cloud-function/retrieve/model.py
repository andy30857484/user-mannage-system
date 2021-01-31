class UserModel():
    def __init__(self, name=None, phone=None, email=None, role="customer", lineId="1"):
        self.name = name
        self.phone = phone
        self.email = email
        self.role = role
        self.lineId = lineId

class UserResponse():
    def __init__(self, userModel=None, result=None):
        self.userModel = userModel
        self.result = result
