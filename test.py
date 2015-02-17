import unittest
import chain

class SquareMap(chain.Map):
    def _map(self, key_value):
        key, value = key_value
        return key, value**2

class Add(chain.Reduce):
    def _reduce(self, key_value):
        key, value = key_value
        return (key, sum(value))

class ChainTest(unittest.TestCase):
    def test_map(self):
        inputs = [(None, 0),(None, 1),(None, 2),(None, 3),(None, 4)]
        expected_output = [(None, sum([0,1,4,9,16]))]
        test_output = chain.run_map_reduce(inputs, 4, [SquareMap], [Add])
        print(test_output)
        assert test_output == expected_output