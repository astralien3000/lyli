
class Symbol(str):
    def __new__(cls, name, type="void"):
        ret = super(Symbol, cls).__new__(cls,name)
        ret.type = type
        return ret
    def escape(c):
        if ord(c) < 128:
            return c
        return "_u" + str(ord(c)) + "_"
    def __str__(self):
        return ''.join(list(map(Symbol.escape, super(Symbol, self).__str__())))

class String(str):
    def __str__(self):
        ret = '"'
        ret += self
        ret += '"'
        return ret
  
class PCall(list):
    def __str__(self):
        ret = "("
        ret += str(self[0])
        for a in self[1:]:
            ret += " "
            ret += str(a)
        ret += ")"
        return ret

class Global(list):
    def __str__(self):
        ret = ""
        ret += str(self[0])
        for a in self[1:]:
            ret += "\n"
            ret += str(a)
        return ret
