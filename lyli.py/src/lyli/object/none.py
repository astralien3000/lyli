from .object import Object


class NoneType(Object):
  def __repr__(self):
    return "NoneType()"

  def py_none(self):
    return None
