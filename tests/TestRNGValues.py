import struct
import unittest
import StringIO
from rngtool import rng_tool, get_argparser


def format_text_output(text):
    values = text.split('\n')
    # remove empty
    values = list(filter(lambda x: x is not '', values))
    # cast to long
    values = list(map(lambda x: long(x), values))
    return values


def format_raw_output(raw):
    return list(struct.unpack('<BBBBBBBBBB', raw))


class TestRNGValues(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRNGValues, self).__init__(*args, **kwargs)
        self.parser = get_argparser()

    def test_test_output(self):
        test_values = [0, 2, 1, 0, 2, 1, 0, 0, 1, 1]

        args = self.parser.parse_args(['-n', '10', '-s', '0xFFFF', '-r', '3'])
        output = StringIO.StringIO()
        rng_tool(args, f_output=output)
        self.assertEqual(test_values, format_text_output(output.getvalue()))

        args = self.parser.parse_args(['-n', '10', '-s', '65535', '-r', '3'])
        output = StringIO.StringIO()
        rng_tool(args, f_output=output)
        self.assertEqual(test_values, format_text_output(output.getvalue()))

    def test_raw_output(self):

        test_values = [9, 216, 112, 32, 236, 107, 28, 81, 115, 90]

        args = self.parser.parse_args(['-n', '80', '-s', '0xFFFF'])
        output = StringIO.StringIO()
        rng_tool(args, f_output_raw=output)
        self.assertEqual(test_values, format_raw_output(output.getvalue()))
