from re import compile as re_compile

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

def valmap(t):
    # TODO: Use a dict for the mapping ?
    # TODO: missing types:
    #  * range
    #  * ...
    if t == dict:
        return objenc
    elif t == list or t == set or t == tuple:
        return arrenc
    elif t == str:
        return strenc
    elif t == int or t == float or t == complex:
        return numenc
    elif t == bool:
        return boolenc
    else:
        return litenc

def valenc(x, max_depth):
    if x == None:
        return LIT_NIL
    else:
        return valmap(type(x))(x, max_depth)

def objenc(x, max_depth):
  return OPEN_BRACE + objenc_internal(x, max_depth) + SHUT_BRACE

def arrenc(a, max_depth):
  max_depth -= 1
  # TODO: Restore num + unit thing ?
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
  # klass = (x.class.ancestors & mapping.keys).first
  # TODO: support mapping
  # if klass
  #   mapping[klass].call(x)
  # else
    return strenc(repr(x))
# rescue
#   klass = (class << x; self; end).ancestors.first
#   strenc("#<#{klass}:0x#{x.__id__.to_s(16)}>")
# end

# def timeenc(t)
#   t.utc.iso8601

# def dateenc(d)
#   d.iso8601

def is_literal(s):
  return (RE_LITERAL.search(s) == None)
