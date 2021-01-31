class DeviceModel():
    def __init__(self, device=None, staff=None, customer=None, rssi=None):
        self.device = device
        self.staff = staff
        self.customer = customer
        self.rssi = rssi


class DeviceResponse():
    def __init__(self, deviceModel=None, result=None):
        self.deviceModel = deviceModel
        self.result = result
