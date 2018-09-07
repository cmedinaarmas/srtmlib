import unittest
import core

class TestCalc(unittest.TestCase):

    def setUp(self):
        # define configuration
        src_file_1arc = 'srtmlib/data/everest/n27_e085_1arc_v3.bil'
        src_file_3arc = 'srtmlib/data/guadaloupe/n15_w062_3arc_v2.bil'

        # instantiate 1-arc-second object
        self.tile_1arc = core.Tile(src_file_1arc,1,0)

        # instantiate 3-arc-second object
        self.tile_3arc = core.Tile(src_file_3arc,3,0)

    def trearDown(self):
        pass

    def test_read_bytes(self):
        bytes_to_read = 2
        result = self.tile_1arc.read_bytes(bytes_to_read)
        self.assertEqual(result[0],117)
        self.assertEqual(result[1],7)

    def test_decode_hgt(self):
        shape = self.tile_1arc.shape
        bytes_to_read = shape[0]*shape[1]*2
        data = self.tile_1arc.read_bytes(bytes_to_read)

        # test default format
        wrapped = False
        heights = self.tile_1arc.decode_hgt(data, wrapped)
        self.assertEqual(heights[0],1909)

        # test wrapped format
        wrapped = True
        heights = self.tile_1arc.decode_hgt(data, wrapped)
        self.assertEqual(heights[0],117)

    def test_load_data(self):

        # test size of loaded heights

        # 1-arc-second
        self.tile_1arc.load_data()
        self.assertEqual(self.tile_1arc.shape,(3601,3601))

        # 3-arc-second
        self.tile_3arc.load_data()
        self.assertEqual(self.tile_3arc.shape,(1201,1201))




if __name__ == '__main__':
    unittest.main()
