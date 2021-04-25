import unittest
import os
import hw_10_1st_add
class TestRunReader(unittest.TestCase):
    def test_run_reader_file_exist(self):
        self.assertIs(os.path.isfile('./LCD1602_chars.txt'), True, "File not exist")

    # то же, но другими словами
    def test_run_reader_file_not_exist(self):
        self.assertIsNot(os.path.isfile('./LCD1602_chars.txt'), False, "File not exist")

    def test_run_reader_return_dict(self):
        self.addTypeEqualityFunc(dict, hw_10_1st_add.run_reader())

    def test_run_reader_is_not_none(self):
        self.assertIsNotNone(hw_10_1st_add.run_reader())

    def test_run_reader_more_null(self):
        self.assertGreater(len(hw_10_1st_add.run_reader()), 0)

    def test_run_reader_at_least_1(self):
        self.assertGreaterEqual(len(hw_10_1st_add.run_reader()), 1)

    def test_run_reader_result1(self):
        self.assertIn('lcd.putchar(chr(168))\n', hw_10_1st_add.run_reader())

    def test_run_reader_result2(self):
        self.assertIn('lcd.putchar(chr(44))\n', hw_10_1st_add.run_reader())

    def test_run_reader_result3(self):
        self.assertIn('lcd.putchar(chr(32))\n', hw_10_1st_add.run_reader())

    def test_run_reader_not_result1(self):
        self.assertNotIn('LCD1602_chars.txt', hw_10_1st_add.run_reader())

    def test_run_reader_not_result2(self):
        self.assertNotIn('lcd.putchar(chr(1))\n', hw_10_1st_add.run_reader())

    def test_run_reader_not_result3(self):
        self.assertNotIn('lcd.putchar(chr(203))\n', hw_10_1st_add.run_reader())
if __name__ == "__main__":
    unittest.main()