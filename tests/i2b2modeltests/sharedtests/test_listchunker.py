import io
import unittest
from contextlib import redirect_stdout

output1 = """.abcdefgh-
.ijklmnop-
.qrstuvwx-
yz-

"""


class ListChunkerTestCase(unittest.TestCase):

    def test_basics(self):
        from i2b2model.shared.listchunker import ListChunker
        lc = ListChunker([], 10)
        for _ in lc:
            self.assertFalse(True, "List should be empty")
        lc = ListChunker([1], 10)
        for c in lc:
            self.assertEqual(c, [1])
        lc = ListChunker(range(10, 20), 10)
        for c in lc:
            self.assertEqual(c, range(10, 20))
        lc = ListChunker(range(10, 21), 10)
        self.assertEqual(lc.__next__(), range(10, 20))
        self.assertEqual(lc.__next__(), range(20, 21))
        with self.assertRaises(StopIteration):
            lc.__next__()

    def test_dots(self):
        from i2b2model.shared.listchunker import ListChunker
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        lc = ListChunker(alphabet, 8)
        output = io.StringIO()
        with redirect_stdout(output):
            for c in lc:
                print(c + '-')
        self.assertEqual(output1, output.getvalue())

        lc = ListChunker(alphabet, 8)
        output = io.StringIO()
        with redirect_stdout(output):
            for _ in lc:
                pass
        self.assertEqual('...\n', output.getvalue())

        lc = ListChunker(alphabet, 8, False)
        output = io.StringIO()
        with redirect_stdout(output):
            for _ in lc:
                pass
        self.assertEqual('', output.getvalue())


if __name__ == '__main__':
    unittest.main()
