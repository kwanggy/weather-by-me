import json

from util import set_timezone, set_dateform, log


conf = {
    'sys': {
        'debug': True,
        'port': 9020,
        'base_url': None,
        'secret_key': None,
        'timezone': 'America/New_York',
        'dateform': '%Y-%m-%d @ %H:%M',
        'verbose': True,
        'timeout': 120,
        'max_tries': 3,
        'test': False,
        'database': None,
        'sender': 'unstoppable.little.spark@gmail.com'
    },
    'upload': {
    },
    'required': {
        'sys': [ 'database' ]
    }
}

def load_conf(filepath):
    __conf__ = None
    with open(filepath) as f:
        r = f.read()
        __conf__ = json.loads(r)

    if __conf__ == None:
        raise Exception('load configuration %s failed' % filepath)

    for key in __conf__:
        c = conf[key]
        _c = __conf__[key]
        for subkey in _c:
            c[subkey] = _c[subkey]

    required = conf['required']
    for req in required:
        c = conf[req]
        for r in required[req]:
            if c[r] == None:
                raise ValueError('conf.%s.%s is None' % (req, r))

    check_test_mode()
    set_timezone(conf['sys']['timezone'])
    set_dateform(conf['sys']['dateform'])

def load_default_conf():
    if check_test_mode():
        load_conf('conf/local.conf')
    else:
        load_conf('conf/prod.conf')

def check_test_mode():
    try:
        with open('TEST') as f:
            pass
        log('TEST MODE')
        conf['sys']['test'] = True
        return conf['sys']['test']
    except:
        pass
    return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        load_conf(sys.argv[1])
        log(conf)
