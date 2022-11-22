import json, platform
from pprint import pprint

def get_sysinfo(*args, **kwargs):
    sysinfo = platform.uname()
    return {
        'name': sysinfo.node,
        'type': sysinfo.system,
        'kernel': sysinfo.version,
        'arch': sysinfo.machine
    }

def post_hello(*args, **kwargs):
    raw_data = args[0].get("wsgi.input").read().decode()
    data = json.loads(raw_data)
    pprint(data)
    return 'Hello, World'

def post_state(*args, **kwargs):
    raw_data = args[0].get("wsgi.input").read().decode()
    data = json.loads(raw_data)
    pprint(data)
    return ''