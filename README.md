# flowrun

Finite-state machine [echoer](https://github.com/yametech/echoer "Markdown") Python  SDK
---------

> pip install flowrun

Action Example
---------

```python
from flowrun.action import Action

action = Action(
    echoer_url='echoer_server_address (http)'
)

# Register action to echoer_server
action.add_data({
    'project': 'str',
    'version': 'str'
})
action.create(
    interface_url='interface_address(http)', name='action_name')

# Get a action info
action.one(name='action_name')

# Get all actions 
action.all()

# Delete a action
action.delete(name='action_name', uuid='action_uuid')

```

FlowRun Example
---------

```python
from flowrun.flowrun import FlowRun

flow = FlowRun(
    echoer_url='echoer_server_address (http)',
)

# Register flow run to echoer_server
flow.add_step(
    name='step_name',
    action='action_name',
    step={'SUCCESS': 'done', 'FAIL': 'done'},
    args={'project': 'https://github.com/yametech/compass.git', 'version': 'v0.1.0'}
)
flow.create(name='flow_name')

# Get a flow info
flow.one(name='flow_name')

# Get all flows 
flow.all()

# Delete a action
flow.delete(name='flow_name', uuid='flow_uuid')

```

Step Example
---------

```python
from flowrun.step import ResponseStep

# Call back result to step
step = ResponseStep(echoer_url='echoer_server_address (http)')
step.response(
    flow_id='flow_id',  # str
    step_name='step_name',  # str
    ack_state='SUCCESS',  # SUCCESS | FAIL | REJECT | NEXT
    uuid='step_uuid',  # str
    done=True  # bool
)
```