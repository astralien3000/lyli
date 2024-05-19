import os
import re
import lark

import lyli.ast._transformer as _transformer


GRAMMAR_PATH = os.path.join(
  os.path.dirname(
    os.path.abspath(__file__)
  ),
  "grammar.lark",
)

with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
  grammar = f.read();

parser = lark.Lark(grammar, start="file", parser="lalr")
trans = _transformer.Transformer()


def clean_comments(code):
  return re.sub(r"\/\/+.*\n|\/\*(.|\n)*\*\/", "", code)


def parse(code: str) -> _transformer._ast.Expr:
  cleaned_code = clean_comments(code)
  raw_ast = parser.parse(cleaned_code)
  expr = trans.transform(raw_ast)
  return expr
