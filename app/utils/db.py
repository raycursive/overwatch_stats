from pymongo import MongoClient
from .classproperty import classproperty
from app.config import MONGO_URL


class Mongo:
    _db = None
    _cx = None

    @classproperty
    def db(cls):
        if cls._db is None:
            cls._cx = MongoClient(MONGO_URL)
            cls._db = cls._cx.get_database()
        return cls._db

    @classmethod
    def close(cls):
        cls._cx.close()
        cls._db = None
        cls._cx = None
