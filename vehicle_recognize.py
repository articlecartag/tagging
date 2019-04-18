import json
import requests
import base64
from PIL import Image
from io import BytesIO
import urllib
import os


def base64_encode(img_path):
    with open(img_path, 'rb') as f:
        data = f.read()
        encodestr = base64.b64encode(data)
        return encodestr

def http_post(url,data_json):
    response = requests.post(url,data_json)
    return response

def url2label(image_url):
    '''
    image_name = image_url.split('/')[-1]
    down_path = './' + image_name
    urllib.request.urlretrieve(image_url, down_path)
    image_base64 = base64_encode(down_path)
    textmod = {"accessKeyId": 'test', "image": image_base64, "fileName": down_path}
    result = http_post('https://ml.yiche.com/recognize//rest/v1/vehicle/identify', textmod)
    json_data = json.loads(result.text)
    carModelId = json_data.get('result')['model']['data'][0]['carModelId']
    conf = json_data.get('result')['model']['data'][0]['prob']
    os.remove(down_path)
    return carModelId,conf
    '''
    response = requests.get(image_url)
    #image = Image.open(BytesIO(response.content))
    ls_f = base64.b64encode(BytesIO(response.content).read())
    textmod = {"accessKeyId": 'test', "image": ls_f, "fileName": 'aaaa'}
    response = requests.post('https://ml.yiche.com/recognize//rest/v1/vehicle/identify', textmod)
    json_data = json.loads(response.text)
    carModelId = json_data.get('result')['model']['data'][0]['carModelId']
    conf = json_data.get('result')['model']['data'][0]['prob']
    return carModelId,conf


# #调用图片地址
# image_url='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1555579877096&di=50598b3cac58a57f6edc342f76319bb4&imgtype=0&src=http%3A%2F%2F04img.mopimg.cn%2Fmobile%2F20180619%2F20180619231754_7ea2567d7691440da8d46109ffdd5f74_1.jpeg'
# carModelId,conf=url2label(image_url)
# print('carModelId:',carModelId,'conf:',conf)


# #调用本地图片
# img_path='./951812c9af4b915e47ad83fc23dda46a.jpeg'
# image_base64=base64_encode(img_path)
# textmod={"accessKeyId":'test' ,"image":image_base64,"fileName":img_path}
# result=http_post('https://ml.yiche.com/recognize//rest/v1/vehicle/identify',textmod)
# json_data=json.loads(result.text)
# carModelId=json_data.get('result')['model']['data'][0]['carModelId']
# conf=json_data.get('result')['model']['data'][0]['prob']
# print('carModelId:',carModelId,'conf:',conf)





