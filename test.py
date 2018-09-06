import unittest
import block as bl

class TestCalc(unittest.TestCase):

    def setUp(self):
        src_file = 'data/everest/n27_e085_1arc_v3.bil'
        self.arc_seconds = 1
        self.b = bl.Block(src_file,1,0)

        self.shape = None
        if self.arc_seconds == 1:
            self.shape = (3601,3601)
        elif self.arc_seconds == 3:
            self.shape = (1201,1201)
        else:
            self.shape = (0,0)
        pass

    def trearDown(self):
        pass

    def test_read_bytes(self):
        bytes_to_read = 2
        result = self.b.read_bytes(bytes_to_read)
        self.assertEqual(result[0],117)
        self.assertEqual(result[1],7)

    def test_decode_hgt(self):
        bytes_to_read = self.shape[0]*self.shape[1]*2
        data = self.b.read_bytes(bytes_to_read)

        # test default format
        wrapped = False
        heights = self.b.decode_hgt(data, wrapped)
        self.assertEqual(heights[0],1909)
        # test wrapped format
        wrapped = True
        heights = self.b.decode_hgt(data, wrapped)
        self.assertEqual(heights[0],117)



if __name__ == '__main__':
    unittest.main()
