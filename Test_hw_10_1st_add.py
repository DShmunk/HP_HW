import unittest
import os
import hw_10_1st_add


class TestRunReader(unittest.TestCase):
    def test_run_reader_file_exist(self):
        self.assertIs(os.path.isfile('./LCD1602_chars.txt'), True, "File exist")

    # то же, но другими словами
    def test_run_reader_file_not_exist(self):
        self.assertIsNot(os.path.isfile('./LCD1602_chars.txt'), False, "File not exist")

    def test_run_reader_return_dict(self):
        self.addTypeEqualityFunc(dict, hw_10_1st_add.run_reader())



if __name__ == "__main__":
    unittest.main()