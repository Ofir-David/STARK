import hashlib
import random
from .field import FieldElement

from typing import Dict, Any


class HashChain:

    @staticmethod
    def _hash(s: str) -> str:
        return hashlib.sha256(s.encode('ascii')).hexdigest()

    def __init__(self, *elements):
        self.hash_seed = 'Jabberwocky'
        self.index = 0
        for elem in elements:
            self.add_randomness(elem)

    def add_randomness(self, elem=''):
        self.hash_seed = HashChain._hash(str(self.hash_seed) + str(elem) + str(self.index))

    def random_int(self, range: int):
        self.add_randomness()
        return int(self.hash_seed, 16) % range

    def randN(self) -> int:
        return self.random_int(FieldElement._p)


class HashChainWriter(HashChain):

    def __init__(self):
        super().__init__()
        self.dict: Dict[str, Any] = {}
        self.counter = 0

    def __setitem__(self, key, value):
        assert isinstance(key, str), 'Key must be a string'
        self.dict[key] = (value, self.counter)
        self.counter += 1
        self.add_randomness(value)


class HashChainReader(HashChain):

    def __init__(self, reader: Dict[str, Any]):
        super().__init__()
        self.reader = reader
        self.counter = 0

    def __getitem__(self, key):
        value, counter = self.reader[key]
        assert counter == self.counter, 'Read values in the wrong order'
        self.counter += 1
        self.add_randomness(value)
        return value
