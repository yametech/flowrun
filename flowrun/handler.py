import json

import requests
from sseclient import SSEClient

from .utils import error_suppress, connect_false, false


class EchoerHandler:

    def __init__(self, url):
        self.action = []
        self.model = []
        self.success_status = []
        self.fail_status = []
        self.url = url
        self.version = 0
        self.first_connect()

    @staticmethod
    def get_flow_name(data):
        with error_suppress(false):
            name = '_'.join(data.split('_')[:-1])
            return name

    def first_connect(self):
        with error_suppress(connect_false):
            data = requests.get(f'{self.url}/flowrun')
            self.version = int(data.json()[-1]['metadata']['version']) - 100

    def add_action(self, action, model, success, fail):
        self.action.append(action)
        self.model.append(model)
        self.success_status.append(success)
        self.fail_status.append(fail)

    def artifact_connect(self):
        # sse长连接请求结果，将实时打印返回的数据响应
        messages = SSEClient(f'{self.url}/watch?resource=flowrun?version={self.version}')
        for msg in messages:
            if msg == "":
                print("返回数据为空")
                continue
            data = json.loads(msg.data)
            version = data['metadata']['version']

            for step in data['spec']['steps']:
                action = step['metadata']['name']
                print(f'检测到action{action}')
            self.version = int(version) - 1
