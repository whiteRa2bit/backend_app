from mafia_resources.db import get_mongo_db, MongoCollection, to_object_id

from mafia_resources.db.config import DATABASE_HOST, DATABASE_NAME
from mafia_resources.utils import create_namedtuple_instance

_db = get_mongo_db(DATABASE_HOST, DATABASE_NAME)


class UsersCollection(MongoCollection):
    FIELDS = create_namedtuple_instance(
        'UsersCollectionFields', username='username', avatar_url='avatar_url',
        gender='gender', email='email', game_ids='game_ids'
    )

    def __init__(self):
        super().__init__(_db.users)

    def add_user(self, user):
        user_id = self._collection.insert(user)
        return user_id

    def get_user(self, user_id):
        obj_id = to_object_id(user_id)
        user = self._collection.find_one({self._ID_FIELD_NAME: obj_id})
        return user

    def get_users(self, user_ids):
        obj_ids = list(map(to_object_id, user_ids))
        if obj_ids:
            users = self._collection.find({self._ID_FIELD_NAME: {'$in': obj_ids}})
        else:
            users = self._collection.find()
        return users

    def update_user(self, user_id, user):
        obj_id = to_object_id(user_id)
        return self._collection.update({self._ID_FIELD_NAME: obj_id}, user)

    def delete_user(self, user_id):
        self._collection.remove({'_id': to_object_id(user_id)})

    @property
    def id_field_name(self):
        return self._ID_FIELD_NAME


users_collection = UsersCollection()
