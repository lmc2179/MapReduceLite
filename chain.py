from multiprocessing import Pool
import copy
import functools
from collections import defaultdict

class Chainable(object):
    def __init__(self, number_of_processes):
        self.pool = Pool(number_of_processes)

    def __getstate__(self):
    # When state of object is requested for pickling, do not return pool (pool objects cannot be pickled)
        self_dict = self.__dict__.copy()
        del self_dict['pool']

    def run(self, inputs):
        raise NotImplementedError

class Map(Chainable):
    def run(self, inputs):
        mapped_key_values = self.pool.starmap(self._map, inputs)
        return functools.reduce(lambda l1,l2:l1+l2, mapped_key_values)

    def _map(self, key, value):
        raise NotImplementedError

class Reduce(Chainable):
    def run(self, key_value_lists):
        return self.pool.starmap(self._reduce, key_value_lists)

    def _reduce(self, key, value):
        raise NotImplementedError

class Sort(Chainable):
    def run(self, key_value_pairs):
        output = defaultdict(list)
        for k,v in key_value_pairs:
            output[k].append(v)
        return output.items()

def run_map_reduce(data, number_of_inputs, map_reduce_pairs):
    data = copy.deepcopy(data)
    for mapper, reducer in map_reduce_pairs:
        mapped_data = mapper(number_of_inputs).run(data)
        sorted_data = Sort(number_of_inputs).run(mapped_data)
        data = reducer(number_of_inputs).run(sorted_data)
    return data


