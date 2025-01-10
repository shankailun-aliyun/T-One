import base64
import time
import traceback
import os
import requests

def get_token(username, token):
    cookie = username + '|' + token + '|' + str(time.time())
    signature = base64.b64encode(cookie.encode('utf-8')).decode('utf-8')
    return signature

def create_job_by_template():
    """ 根据模版创建 job """
  
    username = os.environ.get('INPUT_USERNAME')
    token = os.environ.get('INPUT_TOKEN')
    workspace = os.environ.get('INPUT_WORKSPACE')
    template = os.environ.get('INPUT_TEMPLATE')
    data = {
        "username": username,
        "signature": get_token(username, token),
        "name": "github action test",
        "template": template,
        "workspace": workspace
    }
    url = 'https://tone.openanolis.cn/api/job/create/'
    try:
        req = requests.request(method="post", url=url, json=data, verify=False)
        print(req.text)
    except Exception as e:
        print(f'error: {e}, {traceback.format_exc()}')

create_job_by_template()
