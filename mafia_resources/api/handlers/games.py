from mafia_resources.db.games_collection import games_collection


def object_id_to_game_id(game):
    game['game_id'] = game.pop(games_collection.id_field_name)
    game['game_id'] = str(game['game_id'])
    return game


def get_game(game_id):
    game = games_collection.get_game(game_id)
    game = object_id_to_game_id(game)
    return game


def get_games(game_ids):
    games = games_collection.get_games(game_ids)
    games = list(map(object_id_to_game_id, games))
    return games


def add_game(game_data):
    game_id = games_collection.add_game(game_data)
    return str(game_id)
