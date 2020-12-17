from .utils import error_suppress, false
import requests
import posixpath


class Action:
    def __init__(self, echoer_url):
        self.echoer_url = posixpath.join(echoer_url, 'action')
        self.name = ''
        self.interface_url = ''
        self.params = ''

    def add_data(self, dictData):
        if not isinstance(dictData, dict):
            return False
        length = len(dictData)
        params = '('
        for k, v in dictData.items():
            if str(v) != 'str' and str(v) != 'int':
                return False
            if length == 1:
                params += f'{v} {k})'
            else:
                params += f'{v} {k},'
            length -= 1
        self.params = params
        return True

    def generate(self):
        data = \
            f"""action {self.name}
                  addr = "{self.interface_url}";
                  method = http;
                  args = {self.params};
                  return = (SUCCESS | FAIL | REJECT | NEXT);
                action_end
            """
        return data

    def create(self, interface_url, name):
        self.interface_url = interface_url
        self.name = name

        data = self.generate()
        action_data = {"data": data}
        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'action')
            req = requests.post(req_url, json=action_data, timeout=30)
            if req.status_code == 200:
                return True
            else:
                print('action发送echoer错误', req.json())
                return False

    def one(self, name):
        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'action', name)
            req = requests.get(req_url, timeout=30)
            if req.status_code == 200:
                return True
            else:
                print('发送echoer错误', req.json())
                return False

    def all(self):
        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'action')
            req = requests.get(req_url, timeout=30)
            if req.status_code == 200:
                return req.json()
            else:
                print('发送echoer错误', req.json())
                return None

    def delete(self, name, uuid):
        with error_suppress(false):
            req_url = posixpath.join(self.echoer_url, 'action', name, uuid)
            req = requests.delete(req_url, timeout=30)
            if req.status_code == 200:
                return req.json()
            else:
                print('发送echoer错误', req.json())
                return None
