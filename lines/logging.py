import syslog
from sys import stderr
from sys import stdout
from sys import argv
from copy import copy
from os.path import basename
from collections import OrderedDict
from itertools import chain

from encoder import dumps

NL = "\n"
FN_TYPE = type(lambda: 1)

OUTPUTS = []
CONTEXT = OrderedDict()
DUMPER = None

LOG = None

# TODO: Make sure this is nice to use
# class context(object):
#     def __init__(self, **context):
#         self.context = OrderedDict(context)

#     def __enter__(self):
#         # Setup things
#         pass

#     def __exit__(self, type, value, traceback):
#         # Tear things down
#         pass

#     def log(self, msg=None, **kwargs):
#         log(msg, **self.context.merge(kwargs))

def setup(output=[], context={}):
    global LOG
    LOG = Log(output, context)

def log(msg=None, **kwargs):
    LOG.log(msg, **kwargs)

### Private stuff ###

class Log(object):
    def __init__(self, output, context):
        self.outputs = to_output(output)
        self.context = OrderedDict(context)

    def log(self, msg=None, **kwargs):
        obj = self.__prepare_obj(msg, kwargs)
        for output in self.outputs:
            output.output(obj)

    def __prepare_obj(self, msg, kwargs):
        obj = copy(self.context)
        if msg != None:
            obj['msg'] = msg
        obj.update(kwargs)

        for k in obj.keys():
            v = obj[k]
            if type(v) == FN_TYPE:
                obj[k] = v()

        return obj

def to_output(*outputs):
    x = []
    for output in chain(outputs):
        if hasattr(output, 'output'):
            x.append(output)
        elif type(output) == file:
            x.append(FileOutput(output))
        elif output == 'stdout':
            x.append(FileOutput(stdout))
        elif output == 'stderr':
            x.append(FileOutput(stderr))
        elif output.syslog:
            x.append(SyslogOutput(output))
        elif output == 'syslog':
            x.append(SyslogOutput(syslog))
        else:
            raise 'Unknown outputter'
    return x

PRI2SYSLOG = {
    'emerg': syslog.LOG_EMERG,
    'alert': syslog.LOG_ALERT,
    'crit': syslog.LOG_CRIT,
    'err': syslog.LOG_ERR,
    'error': syslog.LOG_ERR,
    'warn': syslog.LOG_WARNING,
    'warning': syslog.LOG_WARNING,
    'info': syslog.LOG_INFO,
    'notice': syslog.LOG_NOTICE,
    'debug': syslog.LOG_DEBUG,
}

class SyslogOutput(object):
    def __init__(self, syslog=syslog):
        self.syslog = syslog
        self.opened = False

    def output(self, obj):
        self.__prepare_syslog(obj.get('app'))

        obj = copy(obj)
        obj.delete('pid')
        obj.delete('at')
        obj.delete('app')

        pri = obj.delete('pri')
        pri = PRI2SYSLOG.get(pri, syslog.LOG_INFO)
        data = dumps(obj)
        self.syslog.syslog(pri, data)

    def __prepare_syslog(self, app_name):
        if self.opened:
            return
        if not app_name:
            app_name = basename(argv[0])

        self.syslog.openlog(app_name,
                syslog.LOG_PID | syslog.LOG_CONS | syslog.LOG_NDELAY,
                syslog.LOG_USER)

        self.opened = True

class FileOutput(object):
    def __init__(self, file):
        self.file = file

    def output(self, obj):
        data = dumps(obj) + NL
        self.file.write(data)

setup(output=stderr)
