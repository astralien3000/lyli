
class Context(dict):
    def __init__(self, pairs={}, parent=None):
        dict.__init__(self, pairs)
        self.parent = parent
    def search(self, key):
        if key in self:
            return self
        elif self.parent:
            return self.parent.search(key)
        else:
            raise Exception("NOT FOUND : " + str(key))
    def __getitem__(self, key):
        ctx = self.search(key)
        if ctx:
            return dict.__getitem__(ctx, key)
        else:
            return None
    def __setitem__(self, key, val):
        ctx = self.search(key)
        if ctx:
            dict.__setitem__(ctx, key, val)

cur_ctx = Context()
