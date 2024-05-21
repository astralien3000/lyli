import unittest

from lyli import object, eval, prelude, context


class AtomicTestCase(unittest.TestCase):

  TEST_LIST = [
    ("0", object.Integer, 0, "py_int"),
    ("42", object.Integer, 42, "py_int"),
    ('"hello"', object.String, "hello", "py_str"),
    ('""', object.String, "", "py_str"),
    ("'a'", object.Char, "a", "py_str"),
    ("3.14", object.Float, 3.14, "py_float"),
    ("0.0", object.Float, 0.0, "py_float"),
    ("1.0e2", object.Float, 1.0e2, "py_float"),
    ("1.0e-2", object.Float, 1.0e-2, "py_float"),
    ("true", object.Boolean, True, "py_bool"),
    ("false", object.Boolean, False, "py_bool"),
  ]

  def test_atomic(self):
    for code, cls, val, method in self.TEST_LIST:
      with self.subTest(code=code):
        ctx = context.Context(parent=prelude.prelude_ctx)
        res = eval.eval(code, ctx)
        self.assertTrue(isinstance(res, object.Object))
        self.assertTrue(isinstance(res, cls))
        self.assertEqual(getattr(res, method)(), val)

if __name__ == '__main__':
  unittest.main()