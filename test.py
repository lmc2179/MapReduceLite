import unittest
import chain

class Square(chain.Map):
    def _map(self, key_value):
        key, value = key_value
        return [(key, value**2)]

class Add(chain.Reduce):
    def _reduce(self, key_value):
        key, value = key_value
        return (key, sum(value))

class Tokenize(chain.Map):
    def _map(self, key_value):
        key, value = key_value
        tokens = value.split(' ')
        return [(t,1) for t in tokens]

class Count(chain.Reduce):
    def _reduce(self, key_value):
        key,value = key_value
        return (key, sum(value))

class ChainTest(unittest.TestCase):
    def test_sum_of_squares(self):
        inputs = [(None, 0),(None, 1),(None, 2),(None, 3),(None, 4)]
        expected_output = [(None, sum([0,1,4,9,16]))]
        test_output = chain.run_map_reduce(inputs, 4, [(Square,Add)])
        print(test_output)
        assert test_output == expected_output

    def test_word_count(self):
        inputs = [('document 1','a b c'),('document 2','a b c d')]
        expected_output_dict = dict([('a',2),('b',2),('c',2),('d',1)])
        test_output = chain.run_map_reduce(inputs, 4, [(Tokenize,Count)])
        print(test_output)
        assert dict(test_output) == expected_output_dict
