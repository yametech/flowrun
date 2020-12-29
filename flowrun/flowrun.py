import posixpath

import requests

from .step import Step
from .utils import error_suppress, false


class FlowRun:

    def __init__(self, echoer_url):
        self.echoer_url = echoer_url
        self._name = ''
        self._step_list = []
        self._desc = []
        self._step = []

    def add_step(self, name, step, action, args):
        new_step = Step(name=name, action=action)
        desc = new_step.flow_return(step=step, args=args)
        self._step = list(set(self._step).union(set(desc)))
        self._step.sort()
        self._step_list.append(new_step)

    def check_desc(self, desc):
        if not set(self._step).issubset(set(desc.keys())):
            return False
        return True

    def generate(self):
        data = ''
        for step in self._step_list:
            _ = step.generate()
            data += f'  {_}\n'
        return f'flow_run {self._name}\n{data}flow_run_end'

    def create(self, name):
        self._name = name
        a = self.generate()
        a = a.replace('"`', '`')
        a = a.replace('`"', '`')
        flow_data = {'data': a}
        print(flow_data['data'])

        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'flowrun')
            print('req_url', req_url)
            req = requests.post(req_url, json=flow_data, timeout=30)
            if req.status_code == 200:
                return True
            else:
                print('发送echoer错误', req.json())
                return False

    def one(self, name):
        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'flowrun', name)
            print('url', req_url)
            req = requests.get(req_url, timeout=30)
            print('result', req.__dict__)
            if req.status_code == 200:
                return req.json()
            else:
                print('发送echoer错误', req.json())
                return False

    def all(self):
        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'flowrun')
            req = requests.get(req_url, timeout=30)
            if req.status_code == 200:
                return req.json()
            else:
                print('发送echoer错误', req.json())
                return None

    def delete(self, name, uuid):
        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'flowrun', name, uuid)
            print(req_url)
            req = requests.delete(req_url, timeout=30)
            print(req.__dict__)
            if req.status_code == 200:
                return req.json()
            else:
                print('发送echoer错误', req.json())
                return None
