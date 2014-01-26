from re import compile as re_compile
from datetime import date
from datetime import time
from datetime import datetime


def dumps(obj, max_depth=4):
    return objenc_internal(obj, max_depth)

### Private stuff ###


def objenc_internal(obj, max_depth):
    max_depth -= 1
    if max_depth < 0:
        return '...'

    return ' '.join(
        '%s=%s' % (keyenc(k), valenc(v, max_depth)) for k, v in obj.iteritems()
    )


def keyenc(obj, *_):
    if type(obj) == str or type(obj) == unicode:
        return strenc(obj)
    else:
        return strenc(repr(obj))


def valenc(obj, max_depth):
    if obj is None:
        return 'nil'
    elif obj is True:
        return '#t'
    elif obj is False:
        return '#f'

    for t in type(obj).__mro__:
        if t in TYPE_MAP:
            return TYPE_MAP[t](obj, max_depth)

    raise TypeError("BUG")


def objenc(obj, max_depth):
    return '{' + objenc_internal(obj, max_depth) + '}'


def arrenc(obj, max_depth):
    max_depth -= 1
    # TODO: Restore num + unit thing, when a tuple of two elements ?
    # # num + unit. Eg: 3ms
    # if type(obj) == tuple and len(obj) == 2:
    #     return "%s:%s" % (numenc(obj[0]), strenc(obj[1]))

    if max_depth < 0:
        return '[...]'

    return '[' + ' '.join(valenc(x, max_depth) for x in obj) + ']'


def strenc(obj, *_):
    if not is_literal(obj):
        return repr(obj)
    return obj


def numenc(obj, _):
    return str(obj)


def litenc(obj, _):
    return strenc(repr(obj))


def timeenc(obj, _):
    # FIXME: TZ needs to be appended to the output string
    return obj.isoformat()


def is_literal(s):
    return RE_LITERAL.search(s) is None

RE_LITERAL = re_compile(r'[\s\'"=:{}\[\]]')

TYPE_MAP = {
    complex: numenc,
    date: timeenc,
    datetime: timeenc,
    dict: objenc,
    float: numenc,
    int: numenc,
    list: arrenc,
    object: litenc,
    set: arrenc,
    str: strenc,
    time: timeenc,
    tuple: arrenc,
    unicode: strenc,
}
