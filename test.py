import unittest
import Block as bl

class TestCalc(unittest.TestCase):

    def setUp(self):
        src_file = 'data/everest/n27_e085_1arc_v3.bil'
        b = bl.Block(src_file,1,0)
        pass

    def trearDown(self):
        pass

    def test_read_bytes(self):
        result = b.read_bytes(2)
        self.assertEqual(result[0],117)
        self.assertEqual(result[1],7)

if __name__ == '__main__':
    unittest.main()
