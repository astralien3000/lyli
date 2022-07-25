import re

class Expr:
  """
  Base ast expression class.
  Can be either an Atomic or a Call.
  """
  pass


class Atomic(Expr):
  """
  Atomic ast expression class.
  Can be a symbol, a string, a char , an Integer or a Float.
  """
  pass


class Symbol(Atomic):
  __match_args__ = ("val",)

  def __init__(self, val: str):
    assert(isinstance(val, str))
    self.val = val

  def __repr__(self):
    return self.val
  
  @property
  def name(self):
    return self.val


class String(Atomic):
  def __init__(self, val: str):
    assert(isinstance(val, str))
    self.val = val

  def __repr__(self):
    return f'"{self.val}"'

  @property
  def value(self):
    return self.val


class Char(Atomic):
  def __init__(self, val: str):
    assert(isinstance(val, str))
    assert(len(val) == 1)
    self.val = val

  def __repr__(self):
    return f"'{self.val}'"

  @property
  def value(self):
    return self.val


class Integer(Atomic):
  __match_args__ = ("val",)

  def __init__(self, val: str):
    assert(isinstance(val, str))
    self.val = val

  def __repr__(self):
    return self.val

  @property
  def value(self):
    if re.match(r"^\d+$", self.val):
      return int(self.val)
    elif re.match(r"^0x[0-9A-Fa-f]+$", self.val):
      return int(self.val, base=16)
    else:
      raise ValueError(self.val)


class Float(Atomic):
  def __init__(self, val):
    assert(isinstance(val, str))
    self.val = val

  def __repr__(self):
    return self.val

  @property
  def value(self):
    return float(self.val)


class Call(Expr):
  __match_args__ = ("args",)

  def __init__(self, args):
    self.args = args

  def __getitem__(self, i):
    return self.args[i]

  def __repr__(self):
    return f"""({
      " ".join([
        str(arg) for arg in self.args
      ])
    })"""
