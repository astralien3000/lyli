from .object import Object


class List(Object):
  __match_args__ = ("args",)

  def __init__(self, args):
    self.args = args

  def __getitem__(self, i):
    return self.args[i]

  def __repr__(self):
    return f"""[{
      ",".join([
        str(arg) for arg in self.args
      ])
    }]"""