from .object import Object


class Integer(Object):
  def __init__(self, val: str):
    self.val = val

  def __repr__(self):
    return f"Integer({self.val})"

  def py_int(self):
    return int(self.val)


class Float(Object):
  def __init__(self, val: str):
    self.val = val

  def __repr__(self):
    return f"Float({self.val})"

  def py_float(self):
    return float(self.val)


class String(Object):
  def __init__(self, val: str):
    self.val = val

  def __repr__(self):
    return f"String({self.val})"

  def py_str(self):
    return self.val


class Char(Object):
  def __init__(self, val: str):
    self.val = val

  def __repr__(self):
    return f"Char({self.val})"

  def py_str(self):
    return self.val


class Boolean(Object):
  def __init__(self, val: str):
    self.val = val

  def __repr__(self):
    return f"Boolean({self.val})"

  def py_bool(self):
    if self.val == "true":
      return True
    elif self.val == "false":
      return False
    else:
      raise ValueError(f"Unknown boolean value {self.val}")
