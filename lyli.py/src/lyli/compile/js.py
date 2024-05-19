from lyli.ast._ast import (
    Call as C,
    Symbol as S,
    String,
    Integer,
    Float,
)


class Script:
    def __init__(self, body=[]):
        self.body = body
    
    def __repr__(self):
        return f"""Script({
            ", ".join([
                repr(sub) for sub in self.body
            ])
        })"""


class VariableDefinition:
    def __init__(self, id, init):
        self.id = id
        self.init = init

    def __repr__(self):
        return f"""VariableDefinition({
            ", ".join([
                f"id={self.id}",
                f"init={self.init}",
            ])
        })"""


class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"""Identifier(name={self.name})"""


class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"""Identifier(value={self.value})"""


def compile(expr):
    match expr:
        case Integer(value):
            return Literal(
                value=value,
            )
        case C([S("file"), *file_args]):
            return Script(
                body=[
                    compile(file_arg)
                    for file_arg in file_args
                ]
            )
        case C([S("stmt"), S("let"), S(var_name), S("="), value_expr]):
            return VariableDefinition(
                id=Identifier(var_name),
                init=compile(value_expr)
            )
    raise Exception(f"Not supported expr : {expr}")
