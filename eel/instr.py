
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

class PCall(list):
    def __str__(self):
        ret = str(self[0])
        ret += "("
        for a in self[1:]:
            ret += str(a)
            ret += ","
        ret += ")"
        return ret

class BCall(list):
    def __str__(self):
        ret = str(self[0])
        ret += "{"
        for a in self[1:]:
            ret += str(a)
            ret += ";"
        ret += "}"
        return ret

class Global(list):
    def __str__(self):
        ret = ""
        for a in self:
            ret += str(a)
            ret += ";\n"
        return ret
