import bson
import pymongo


def get_mongo_client(host_or_hosts, **kwargs):
    return pymongo.MongoClient(host_or_hosts, **kwargs)


def get_mongo_db(host_or_hosts, mongo_db, **kwargs):
    client = get_mongo_client(host_or_hosts, **kwargs)
    return client[mongo_db]


def to_object_id(value):
    if isinstance(value, bson.objectid.ObjectId):
        return value
    if isinstance(value, str) and bson.ObjectId.is_valid(value):
        return bson.objectid.ObjectId(value)

    raise ValueError('Can\'t create ObjectId from "{}"'.format(value))
