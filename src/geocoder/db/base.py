# python 3
"""
Abstract base class for database operations.

This class defines the interface for basic database operations such as
getting, deleting, and putting key-value pairs. Subclasses must implement
the following abstract methods:

Methods
-------
get(k)
    Retrieve the value associated with the key `k`.
delete(k)
    Delete the key-value pair associated with the key `k`.
put(k, v)
    Store the key-value pair (`k`, `v`) in the database.

Parameters
----------
k : Any
    The key used to identify the value in the database.
v : Any
    The value to be stored in the database (only for `put` method).
"""
# -*- coding: utf-8 -*-
from abc import *


class DbBase(metaclass=ABCMeta):
    @abstractmethod
    def get(self, k):
        pass

    @abstractmethod
    def delete(self, k):
        pass

    @abstractmethod
    def put(self, k, v):
        pass
