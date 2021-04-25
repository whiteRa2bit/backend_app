from mafia_resources.db import get_mongo_db, MongoCollection, to_object_id

from mafia_resources.db.config import DATABASE_HOST, DATABASE_NAME
from mafia_resources.utils import create_namedtuple_instance

_db = get_mongo_db(DATABASE_HOST, DATABASE_NAME)


class GamesCollection(MongoCollection):
    FIELDS = create_namedtuple_instance(
        'GamesCollectionFields', status='status', game_time='game_time'
    )

    def __init__(self):
        super().__init__(_db.games)

    def add_game(self, game):
        game_id = self._collection.insert(game)
        return game_id

    def get_game(self, game_id):
        obj_id = to_object_id(game_id)
        game = self._collection.find_one({self._ID_FIELD_NAME: obj_id})
        return game

    def get_games(self, game_ids):
        obj_ids = list(map(to_object_id, game_ids))
        if obj_ids:
            games = self._collection.find({self._ID_FIELD_NAME: {'$in': obj_ids}})
        else:
            games = self._collection.find()
        return games

    @property
    def id_field_name(self):
        return self._ID_FIELD_NAME


games_collection = GamesCollection()
