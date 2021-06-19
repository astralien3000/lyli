
class Object:
  def __init__(self, val, typename):
    self.type = typename
    self.val = val
  def __str__(self):
    return str(self.val)