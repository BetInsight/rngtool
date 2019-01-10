import unittest
from rngtool import get_argparser


class TestOptions(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestOptions, self).__init__(*args, **kwargs)
        self.parser = get_argparser()

    def test_all(self):
        args = self.parser.parse_args(['-n', '10000'])
        self.assertEqual(10000, args.seq_length)

        args = self.parser.parse_args(['-n', '10000', '-rw'])
        self.assertTrue(args.raw_output)

        args = self.parser.parse_args(['-n', '10000', '-r', '1000'])
        self.assertEqual(1000, args.seq_range)

    def test_args_convert(self):
        args = self.parser.parse_args(['-n', '10000', '-s', '255'])
        self.assertEqual(255, args.seed)

        args = self.parser.parse_args(['-n', '10000', '-s', '0xFF'])
        self.assertEqual(255, args.seed)
        args = self.parser.parse_args(['-n', '10000', '-s', '0XFF'])
        self.assertEqual(255, args.seed)

        args = self.parser.parse_args(['-n', '10000', '-s', '0b11111111'])
        self.assertEqual(255, args.seed)
        args = self.parser.parse_args(['-n', '10000', '-s', '0B11111111'])
        self.assertEqual(255, args.seed)
