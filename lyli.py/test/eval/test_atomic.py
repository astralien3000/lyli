import unittest

from lyli import object, eval, prelude, context


class AtomicTestCase(unittest.TestCase):

  def test_integer_zero(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("0", ctx)
    self.assertTrue(isinstance(res, object.Integer))
    self.assertEqual(res.py_int(), 0)

  def test_integer_positive(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("42", ctx)
    self.assertTrue(isinstance(res, object.Integer))
    self.assertEqual(res.py_int(), 42)

  def test_string(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval('"hello"', ctx)
    self.assertTrue(isinstance(res, object.String))
    self.assertEqual(res.py_str(), "hello")
  
  def test_string_empty(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval('""', ctx)
    self.assertTrue(isinstance(res, object.String))
    self.assertEqual(res.py_str(), "")
  
  def test_char(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("'a'", ctx)
    self.assertTrue(isinstance(res, object.Char))
    self.assertEqual(res.py_str(), "a")

  def test_char_empty(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    with self.assertRaises(Exception):
      eval.eval("''", ctx)

  def test_float(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("3.14", ctx)
    self.assertTrue(isinstance(res, object.Float))
    self.assertEqual(res.py_float(), 3.14)
  
  def test_float_zero(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("0.0", ctx)
    self.assertTrue(isinstance(res, object.Float))
    self.assertEqual(res.py_float(), 0.0)
  
  def test_float_scientific_pos_pow(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("1.0e2", ctx)
    self.assertTrue(isinstance(res, object.Float))
    self.assertEqual(res.py_float(), 1.0e2)

  def test_float_scientific_neg_pow(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("1.0e-2", ctx)
    self.assertTrue(isinstance(res, object.Float))
    self.assertEqual(res.py_float(), 1.0e-2)
  
  def test_bool_true(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("true", ctx)
    self.assertTrue(isinstance(res, object.Boolean))
    self.assertEqual(res.py_bool(), True)
  
  def test_bool_false(self):
    ctx = context.Context(parent=prelude.prelude_ctx)
    res = eval.eval("false", ctx)
    self.assertTrue(isinstance(res, object.Boolean))
    self.assertEqual(res.py_bool(), False)


if __name__ == '__main__':
  unittest.main()