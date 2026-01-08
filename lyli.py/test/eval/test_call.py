import unittest

import io
import sys

from lyli import object, eval, prelude, context


class IOTape:
  def __init__(self):
    self.stdout = sys.stdout
    self.stringio = io.StringIO()
    sys.stdout = self.stringio
  
  def __enter__(self):
    return self
  
  def __exit__(self, *args):
    sys.stdout = self.stdout



class AtomicTestCase(unittest.TestCase):

  TEST_PRINT_LIST = [
    ('"Hello, world !"', "Hello, world !\n"),
    ("0", "0\n"),
    ("42", "42\n"),
    ("3.14", "3.14\n"),
    ("true", "true\n"),
    ("false", "false\n"),
  ]

  def test_call_print(self):
    for txt_in, txt_out in self.TEST_PRINT_LIST:
      with self.subTest(txt=txt_in):
        ctx = context.Context(parent=prelude.prelude_ctx)
        with IOTape() as iotape:
          res = eval.eval(f"print({txt_in})", ctx)
        self.assertTrue(isinstance(res, object.Object))
        self.assertTrue(isinstance(res, object.NoneType))
        self.assertEqual(iotape.stringio.getvalue(), txt_out)


if __name__ == '__main__':
  unittest.main()