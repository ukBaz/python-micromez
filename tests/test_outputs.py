import unittest
from unittest.mock import patch
from tests import mock_mraa


class TestOutputs(unittest.TestCase):

    def setUp(self):
        # self.mraa_mock = MagicMock()
        self.mraa_mock = mock_mraa.mraa()
        modules = {
            'mraa': self.mraa_mock,
        }
        # self.mraa_mock.getVersion = mock_get_version
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        from micromez import outputs

        self.module_under_test = outputs

    def tearDown(self):
        self.module_patcher.stop()

    def test_canvas_clear_fill(self):
        all_zero = [0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0]
        all_ones = [255, 255, 255, 255, 255, 255, 255, 255,
                    255, 255, 255, 255, 255, 255, 255, 255]
        canvas = self.module_under_test.Grid(16, 8)
        self.assertEqual(all_zero, canvas.memory_map)
        canvas.all_on()
        self.assertEqual(all_ones, canvas.memory_map)

    def test_draw_square(self):
        all_zero = [0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0]
        square = [0, 254, 254, 254, 254, 254, 254, 254,
                  0, 0, 0, 0, 0, 0, 0, 0]
        rectangle = [0, 0, 56, 56, 56, 56, 56, 56,
                     56, 56, 56, 56, 56, 56, 0, 0]
        canvas = self.module_under_test.Grid(16, 8)
        canvas.draw_square(1, 1, 7, 7)
        self.assertEqual(canvas.memory_map, square)
        canvas.draw_square(1, 1, 7, 7, False)
        self.assertEqual(canvas.memory_map, all_zero)
        canvas.draw_square(2, 3, 12, 3)
        self.assertEqual(canvas.memory_map, rectangle)
        with self.assertRaises(ValueError):
            canvas.draw_square(7, 7, 8, 8)

    def test_rotate(self):
        canvas = self.module_under_test.Grid(16, 8)
        pixmap = [(1, 1, 1, 1, 0),
                  (1, 0, 0, 0, 0),
                  (1, 1, 1, 0, 0),
                  (1, 0, 0, 0, 0),
                  (1, 1, 1, 1, 1)]
        pixmap90 = [(1, 1, 1, 1, 1),
                    (1, 0, 1, 0, 1),
                    (1, 0, 1, 0, 1),
                    (1, 0, 0, 0, 1),
                    (1, 0, 0, 0, 0)]
        pixmap180 = [(1, 1, 1, 1, 1),
                     (0, 0, 0, 0, 1),
                     (0, 0, 1, 1, 1),
                     (0, 0, 0, 0, 1),
                     (0, 1, 1, 1, 1)]
        pixmap270 = [(0, 0, 0, 0, 1),
                     (1, 0, 0, 0, 1),
                     (1, 0, 1, 0, 1),
                     (1, 0, 1, 0, 1),
                     (1, 1, 1, 1, 1)]

        r90 = canvas.rotate(pixmap, 90)
        self.assertListEqual(pixmap90, r90)
        r180 = canvas.rotate(pixmap, 180)
        self.assertListEqual(pixmap180, r180)
        r270 = canvas.rotate(pixmap, 270)
        self.assertListEqual(pixmap270, r270)
        r360 = canvas.rotate(pixmap, 360)
        self.assertListEqual(pixmap, r360)


if __name__ == '__main__':
    unittest.main()
