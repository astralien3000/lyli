
class Context:

  def __init__(self, object_dict={}, parent=None):
    self.object_dict = object_dict
    self.parent = parent

  def __getitem__(self, key):
    # print(f"{key} in {list(self.object_dict)}")
    if key == ".":
      path = ["."]
    else:
      path = key.split(".")
    if path[0] in self.object_dict:
      if len(path) == 1:
        return self.object_dict[path[0]]
      else:
        return self.object_dict[path[0]].ctx[
          ".".join(path[1:])
        ]
    elif self.parent:
      return self.parent[key]
    else:
      raise Exception(f"NOT FOUND : {key}")

  def __setitem__(self, key, val):
    self.object_dict[key] = val
  
  def __contains__(self, key):
    return (
      (key in self.object_dict) or
      (
        (self.parent is not None) and
        (key in self.parent)
      )
    )
  
  def update(self, update_dict):
    self.object_dict.update(update_dict)

cur_ctx = Context()
