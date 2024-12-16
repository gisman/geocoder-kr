import leveldb
import json
from geocoder.db.base import DbBase


class LevelDbGeocode(DbBase):
    """
    A class to interact with LevelDB for geocoding purposes.
    """

    ldb = None  # leveldb.LevelDB(db_name, **kwargs)

    def __init__(self, db_name, **kwargs):
        """
        Initialize the LevelDbGeocode instance and open the LevelDB database.

        :param db_name: The name of the database.
        :param kwargs: Additional arguments for LevelDB.
        """
        if not LevelDbGeocode.ldb:
            LevelDbGeocode.ldb = leveldb.LevelDB(db_name, **kwargs)

    def get(self, k):
        """
        Retrieve a value from the database by key.

        :param k: The key to retrieve the value for.
        :return: The value associated with the key.
        """
        if type(k) == bytes:
            return self.ldb.Get(k)
        else:
            return self.ldb.Get(k.encode())

    def delete(self, k):
        """
        Delete a key-value pair from the database.

        :param k: The key to delete.
        """
        if type(k) == bytes:
            self.ldb.Delete(k)
        else:
            self.ldb.Delete(k.encode())

    def put(self, k, json_val):
        """
        Store a key-value pair in the database.

        :param k: The key to store the value under.
        :param json_val: The value to store, which will be converted to JSON.
        """
        if type(k) == bytes:
            self.ldb.Put(k, json_val)
        else:
            self.ldb.Put(k.encode(), json.dumps(json_val).encode("utf8"))
