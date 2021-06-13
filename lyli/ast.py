import lyli.literal

class Expr:
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
  def __str__(self):
    return self.val

class Integer(Atomic):
  def __init__(self, val):
    self.str = val
    self.val = lyli.literal.get_int(val)
    self.type = lyli.literal.get_int_type(val)
  def __str__(self):
    return str(self.val) + str(self.type)

class Float(Atomic):
  def __init__(self, val):
    self.str = val
    self.val = lyli.literal.get_float(val)
    self.type = lyli.literal.get_float_type(val)
  def __str__(self):
    return str(self.val) + str(self.type)

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
