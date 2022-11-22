import json, platform
from pprint import pprint

def get_sysinfo(state):
    sysinfo = platform.uname()
    return {
        'name': sysinfo.node,
        'type': sysinfo.system,
        'kernel': sysinfo.version,
        'arch': sysinfo.machine
    }

def post_hello(data, state):
    return 'Hello, World'

def post_state(data, state):
    return data, data['state']

def get_state(state):
    return {
        'state': state
    }