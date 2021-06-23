import lyli.type

class Expr(lyli.type.Object):
  pass

class Atomic(Expr):
  pass

class Symbol(Atomic):
  def __init__(self, name):
    self.name = name
    lyli.type.Object.__init__(self, self, "ast.Symbol")
  def escape(c):
    if ord(c) < 128:
      return c
    return "_u" + str(ord(c)) + "_"
  def __str__(self):
    return ''.join(list(map(Symbol.escape, self.name)))

class String(Atomic):
  def __init__(self, val):
    self.val = val
    lyli.type.Object.__init__(self, val, "str")
  def __str__(self):
    return self.val

class Char(Atomic):
  def __init__(self, val):
    self.val = val
    lyli.type.Object.__init__(self, val, "char")
  def __str__(self):
    return self.val

class Integer(Atomic):
  def split_int(str):
    prefix = None
    body = str
    if str[:2] in ["0b","0o","0d","0x"]:
      prefix = str[:2]
      body = str[2:]
    return (prefix, body)
  def get_int_base(str):
    prefix = Integer.split_int(str)[0]
    convert = {
      None : 10,
      "0b" : 2,
      "0o" : 8,
      "0d" : 10,
      "0x" : 16,
    }
    return convert[prefix]
  def get_int(str):
    base = Integer.get_int_base(str)
    body = Integer.split_int(str)[1]
    return int(body, base)
  def __init__(self, val):
    self.str = val
    self.int = Integer.get_int(val)
    lyli.type.Object.__init__(self, self.int, "int")
  def __str__(self):
    return str(self.val)

class Float(Atomic):
  def __init__(self, val):
    self.str = val
    self.val = float(val)
    lyli.type.Object.__init__(self, val, "float")
  def __str__(self):
    return str(self.val)

class Call(Expr):
  def __init__(self, items):
    self.items = items
    lyli.type.Object.__init__(self, self, "ast.Call")
  def __getitem__(self, i):
    return self.items[i]
  def __str__(self):
    ret = "("
    ret += str(self.items[0])
    for a in self.items[1:]:
      ret += " "
      ret += str(a)
    ret += ")"
    return ret
