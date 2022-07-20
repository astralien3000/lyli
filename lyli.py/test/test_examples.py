import unittest
import os
import glob

from lyli.__main__ import main


class ExamplesTestCase(unittest.TestCase):
  def test_all(self):
    test_path = os.path.relpath(os.path.dirname(__file__))
    examples_path = os.path.join(os.path.dirname(test_path), "examples")
    examples_glob_path = os.path.join(examples_path, "**", "*.ly")
    for file_path in glob.glob(examples_glob_path, recursive=True):
      with self.subTest(file=file_path):
        main([file_path])
