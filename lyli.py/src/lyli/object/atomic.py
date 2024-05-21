from .object import Object


class Integer(Object):
  def __init__(self, val: int):
    self.val = val

  def __repr__(self):
    return f"Integer({self.val})"


class Float(Object):
  def __init__(self, val: float):
    self.val = val

  def __repr__(self):
    return f"Float({self.val})"


class String(Object):
  def __init__(self, val: str):
    self.val = val

  def __repr__(self):
    return f"String({self.val})"


class Char(Object):
  def __init__(self, val: str):
    self.val = val

  def __repr__(self):
    return f"Char({self.val})"
