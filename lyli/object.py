import lyli.context as context

class Object:
  def __init__(self, val, typ, ctx=context.Context()):
    self.val = val
    self.typ = typ
    self.ctx = ctx
  def __str__(self):
    return str(self.val) + ":" + str(self.typ)
