class MongoCollection(object):
    _ID_FIELD_NAME = '_id'

    def __init__(self, collection):
        self._collection = collection
