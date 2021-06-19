import lyli.literal
import lyli.type

class Expr(lyli.type.Object):
  pass

class Atomic(Expr):
  pass

class Symbol(Atomic):
  def __init__(self, name):
    self.name = name
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
  def __init__(self, val):
    self.str = val
    self.val = lyli.literal.get_int(val)
    lyli.type.Object.__init__(self, val, "integer")
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
