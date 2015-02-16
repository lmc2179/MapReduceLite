from multiprocessing import Pool
import copy

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
        return self.pool.map(self._map, inputs)

    def _map(self, input_object):
        raise NotImplementedError

def run_chain(data, number_of_inputs, chainable_classes):
    data = copy.deepcopy(data)
    for chainable in chainable_classes:
        chainable_object = chainable(number_of_inputs)
        data = chainable_object.run(data)
    return data


