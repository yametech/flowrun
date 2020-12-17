from .utils import error_suppress, false
import posixpath
import requests


class Step:

    def __init__(self, name, action):
        self._flow = None
        self._str_args = None
        self._desc = None

        self._name = name
        self._action = action

    def flow_return(self, step, args=None):
        flow = ''
        for key in step.keys():
            if flow:
                flow += ' | '
            flow += f'{key}->{step[key]}'

        str_args = ''
        if isinstance(args, dict):
            for key in args.keys():
                if str_args:
                    str_args += ','
                value = f'{args[key]}' if isinstance(args[key], int) else f'"{args[key]}"'
                str_args += f'{key}={value}'

        self._flow = flow
        self._str_args = str_args
        self._desc = list(step.values())
        return [self._name]

    def generate(self):
        _ = f'step {self._name} => ({self._flow}) {{action = "{self._action}"; args = ({self._str_args});}};'

        return _


class ResponseStep:

    def __init__(self, echoer_url):
        self.echoer_url = echoer_url

    def response(
            self,
            flow_id,
            step_name,
            ack_state,
            uuid,
            done: bool,
    ):
        with error_suppress(false):
            data = dict(
                flowId=flow_id,
                stepName=step_name,
                ackState=ack_state,
                uuid=uuid,
                done=done
            )

            req_url = posixpath.join(self.echoer_url, 'step')
            req = requests.post(req_url, json=data, timeout=30)
            if req.status_code == 200:
                return req.json()
            else:
                print('发送echoer错误', req.json())
                return None
