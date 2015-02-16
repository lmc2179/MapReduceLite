import unittest
import chain

class SquareMap(chain.Map):
    def _map(self, input_object):
        return input_object**2

class ChainTest(unittest.TestCase):
    def test_map(self):
        inputs = [0,1,2,3,4]
        expected_output = [0,1,4,9,16]
        test_output = chain.run_chain(inputs, 4, [SquareMap])
        assert test_output == expected_output