
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
    self.val = val
  def __str__(self):
    return str(self.val)

class Call(list):
    def __str__(self):
        ret = "("
        ret += str(self[0])
        for a in self[1:]:
            ret += " "
            ret += str(a)
        ret += ")"
        return ret
