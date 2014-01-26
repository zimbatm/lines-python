from re import compile as re_compile
from datetime import date
from datetime import time
from datetime import datetime

SPACE = ' '
LIT_TRUE = '#t'
LIT_FALSE = '#f'
LIT_NIL = 'nil'
OPEN_BRACE = '{'
SHUT_BRACE = '}'
OPEN_BRACKET = '['
SHUT_BRACKET = ']'
SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'

RE_LITERAL = re_compile(r'[\s\'"=:{}\[\]]')

# This is the only "public" function
def dumps(obj, max_depth=4):
    return objenc_internal(obj, max_depth)

### Private stuff ###

def objenc_internal(obj, max_depth):
    max_depth -= 1
    if max_depth < 0:
        return '...'
    
    return SPACE.join("%s=%s" % (keyenc(k), valenc(v, max_depth)) for k,v in obj.iteritems())

def keyenc(k, *_):
    if type(k) == str:
        return strenc(k)
    else:
        return strenc(str(k))

def valenc(x, max_depth):
    if x == None:
        return LIT_NIL
    
    for t in type(x).__mro__:
        if t in MAPPING:
            return MAPPING[t](x, max_depth)

    raise 'BUG, object should be ancestor of all'

def objenc(x, max_depth):
  return OPEN_BRACE + objenc_internal(x, max_depth) + SHUT_BRACE

def arrenc(a, max_depth):
  max_depth -= 1
  # TODO: Restore num + unit thing, when a tuple of two elements ?
  # # num + unit. Eg: 3ms
  # if a.size == 2 && a.first.kind_of?(Numeric) && is_literal?(a.last.to_s)
  #   "#{numenc(a.first)}:#{strenc(a.last)}"
  if max_depth < 0:
    return '[...]'
  else:
    return OPEN_BRACKET + SPACE.join(valenc(x, max_depth) for x in a) + SHUT_BRACKET

def strenc(s, *_):
  s = str(s)
  if not is_literal(s):
    return repr(s)
    # s = s.inspect
    # unless s[1..-2].include?(SINGLE_QUOTE)
    #   s.gsub!(SINGLE_QUOTE, "\\'")
    #   s.gsub!('\"', DOUBLE_QUOTE)
    #   s[0] = s[-1] = SINGLE_QUOTE
    # end
  return s

def boolenc(b, _):
    if b:
        return LIT_TRUE
    else:
        return LIT_FALSE

def numenc(n, _):
  #case n
  # when Float
  #   "%.3f" % n
  #else
    return str(n)
  #end

def litenc(x, _):
    return strenc(repr(x))

def timeenc(x, _):
    # FIXME: TZ needs to be appended to the output string
    return x.isoformat()

def is_literal(s):
  return (RE_LITERAL.search(s) == None)


MAPPING = {
    bool: boolenc,
    complex: numenc,
    dict: objenc,
    float: numenc,
    int: numenc,
    list: arrenc,
    object: litenc,
    set: arrenc,
    str: strenc,
    time: timeenc,
    date: timeenc,
    datetime: timeenc,
    tuple: arrenc,
}
