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
        req = requests.request(method="post", url=url, json=data)
        # print(req.text)
        job_id = req.json().get('data', dict()).get('id')
        job_link = req.json().get('data', dict()).get('job_link')
        if job_id:
            print('job create success, job_id: {}, job_link: {}'.format(job_id, job_link))
            return job_id
    except Exception as e:
        print(f'job create error: {e}, {traceback.format_exc()}')

    return None


def query_job_by_id(job_id):
    """ 查询测试任务状态 """

    username = os.environ.get('INPUT_USERNAME')
    token = os.environ.get('INPUT_TOKEN')

    data = dict(
        username=username,
        signature=get_token(username, token),
        job_id=job_id,
    )

    url = 'https://tone.openanolis.cn/api/job/query/'

    req = requests.request(method="post", url=url, json=data)
    code = req.json().get('code')
    if code != 200:
        print('query job error, code is not 200')
        return None
    else:
        data = req.json().get('data', dict())
        job_state = data.get('job_state', 'running')

        return job_state


def check_job_status(job_id):

    if not job_id:
        return

    while True:
        try:
            job_state = query_job_by_id(job_id)
            if job_state in ['complete', 'fail', 'success', 'stop']:
                print('job finished')
                break
            elif job_state == 'running':
                print('running')
        except Exception as e:
            print('job query error: {}, {}'.format(e, traceback.format_exc()))
            break
        time.sleep(3)


job_id = create_job_by_template()
check_job_status(job_id)
