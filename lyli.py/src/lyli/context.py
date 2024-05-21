class Context:

  def __init__(self, parent=None, data={}):
    self.parent = parent
    self.data = data

  def __getitem__(self, key):
    if key in self.data:
      return self.data[key]
    elif self.parent is not None:
      return self.parent[key]
    else:
      raise KeyError(key)

  def __setitem__(self, key, val):
    self.data[key] = val

  def __contains__(self, key):
    return (
      (key in self.data) or
      (
        (self.parent is not None) and
        (key in self.parent)
      )
    )

  def update(self, update_dict):
    self.data.update(update_dict)

  def keys(self):
    return [
      *self.parent.keys(),
      *self.data.keys(),
    ]

  def values(self):
    return [
      *self.parent.values(),
      *self.data.values(),
    ]

  def items(self):
    return [
      *self.parent.items(),
      *self.data.items(),
    ]

  def __repr__(self):
    return repr({k: v for k, v in self.items()})
