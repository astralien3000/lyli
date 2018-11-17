
class Symbol(str):
    pass

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
