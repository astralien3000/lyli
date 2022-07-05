import os
import re
import lark

import lyli.transformer as transformer


GRAMMAR_PATH = os.path.join(
  os.path.dirname(
    os.path.abspath(__file__)
  ),
  "grammar.lark",
)

with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
  grammar = f.read();

parser = lark.Lark(grammar, start="file", parser="lalr")
trans = transformer.Transformer()


def clean_comments(code):
  return re.sub(r"\/\/+.*\n|\/\*(.|\n)*\*\/", "", code)


def parse(code: str) -> transformer.ast.Expr:
  cleaned_code = clean_comments(code)
  raw_ast = parser.parse(cleaned_code)
  expr = trans.transform(raw_ast)
  return expr


def parse_file(filename: os.path) -> transformer.ast.Expr:
  with open(filename, "r", encoding="utf-8") as f:
    return parse(f.read())
