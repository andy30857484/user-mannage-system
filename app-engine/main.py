import os
from flask import Flask, request, render_template
import requests
import json
from model import DeviceModel
import dmsConfig

app = Flask(__name__)


deviceModel = DeviceModel()


@app.route("/dms/index", methods=['GET'])
def index():
    global deviceModel
    try:
        deviceModel.device = request.values['device']
    except:
        pass
    return render_template("index.html", deviceModel=deviceModel)


@app.route("/dms/create", methods=['GET', 'POST'])
def create():
    global deviceModel
    if request.method == "GET":

        return render_template("createDeviceRequest.html", deviceModel=deviceModel)
    if request.method == 'POST':

        deviceModel = DeviceModel(request.values['device'], request.values['staff'],
                              request.values['customer'],
                                 request.values['rssi'])

        apiResponse = requests.post(
            dmsConfig.createApi, json=deviceModel.__dict__)

        deviceResponse = apiResponse.json()

        if deviceResponse['result']['code'] == "1":
            return render_template("createDeviceResponse.html", deviceModel=deviceResponse)
        else:
            return render_template("createDeviceFail.html", result=deviceResponse)


@app.route('/dms/update', methods=['GET', 'POST'])
def update():
    global deviceModel
    if request.method == "GET":
        return render_template("queryDeviceRequest.html")
    if request.method == "POST":
        try:
            deviceModel = DeviceModel(request.values['device'], request.values['staff'],
                              request.values['customer'], request.values['rssi'])
            apiResponse = requests.put(dmsConfig.updateApi, json=deviceModel.__dict__)
            deviceResponse = apiResponse.json()
            if deviceResponse['deviceModel']!={}:
                return render_template('updateDeviceResponse.html', deviceModel=deviceResponse)
        except:
            apiResponse = requests.get(dmsConfig.queryApi+'?staff='+request.values['staff'])
            deviceResponse = apiResponse.json()
            if deviceResponse['deviceModel']!={}:
                return render_template('updateDeviceRequest.html', deviceModel=deviceResponse)
            else:
                return render_template('queryDeviceFail.html', deviceModel=deviceResponse)

@app.route('/dms/query', methods=['GET', 'POST'])
def query():
    #global deviceModel
    if request.method == "GET":
        return render_template("queryDeviceRequest.html")
    if request.method == "POST":
        apiResponse = requests.get(dmsConfig.queryApi+'?staff='+request.values['staff'])

        deviceResponse = apiResponse.json()
        if deviceResponse['deviceModel']!={}:
            return render_template('queryDeviceResponse.html', deviceModel=deviceResponse)
        else:
            return render_template('queryDeviceFail.html', deviceModel=deviceResponse)

@app.route('/dms/list', methods=['GET', 'POST'])
def list():
    apiResponse = requests.get(dmsConfig.listApi)

    deviceResponse = apiResponse.json()
    deviceLength = len(deviceResponse['deviceModel'])

    return render_template('listDeviceResponse.html', deviceModel=deviceResponse, length=deviceLength)


@app.route('/dms/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "GET":
        return render_template("deleteDeviceRequest.html")
    if request.method == 'POST':
        deviceModel = DeviceModel(staff=request.values['staff'])

        deviceResponse = requests.delete(
            dmsConfig.deleteApi, json=deviceModel.__dict__)

        deviceResponse = deviceResponse.json()

        if deviceResponse['result']['code'] == "1":
            return render_template("deleteDeviceResponse.html", deviceModel=deviceResponse)
        else:
            return render_template("deleteDeviceFail.html", result=deviceResponse)


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='127.0.0.1', port=port)
