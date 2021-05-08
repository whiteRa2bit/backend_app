import traceback

from flask import Flask, request, jsonify, send_file
from loguru import logger
from werkzeug.exceptions import BadRequest

from mafia_resources.api.handlers import users as users_handler, games as games_handler
from mafia_resources.api.config import USERS_ENDPOINT, USER_STATS_ENDPOINT, GAMES_ENDPOINT, BASE_URL, \
    HEALTCHECK_ENDPOINT
from mafia_resources.api.schema import request_schema, response_schema
from mafia_resources.api.schema.user_schema import UserResponseSchema, \
    UserIdsSchema, UsersResponseSchema, \
    AddUserSchema, AddUserResponseSchema, \
    PatchUserSchema, \
    UserStatsResponseSchema
from mafia_resources.api.schema.game_schema import GameResponseSchema, \
    GameIdsSchema, GameResponsesSchema, \
    AddGameSchema, AddGameResponseSchema
from mafia_resources.config import USER_STATS_DIR


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route(HEALTCHECK_ENDPOINT, methods=['GET'])
    def healtcheck():
        return 'hello', 200

    @app.route(f'{USERS_ENDPOINT}/<string:user_id>', methods=['GET'])
    @response_schema(UserResponseSchema())
    def get_user(user_id):
        logger.info(f'Recieved get_user request for id: {user_id}')
        user = users_handler.get_user(user_id)
        logger.info(f'User with id {user_id}: {user}')

        return jsonify(user), 200

    @app.route(USERS_ENDPOINT, methods=['GET'])
    @request_schema(UserIdsSchema())
    @response_schema(UsersResponseSchema())
    def get_users():
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        user_ids = request.json['user_ids']
        logger.info(f'Recieved get_users request for ids: {user_ids}')
        users = users_handler.get_users(user_ids)
        logger.info(f'Find users: {users}')

        return jsonify({'users': users}), 200

    @app.route(USERS_ENDPOINT, methods=['POST'])
    @request_schema(AddUserSchema())
    @response_schema(AddUserResponseSchema())
    def add_user():
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        user_data = request.get_json()
        logger.info(f'Received add_user request: {user_data}')
        user_id = users_handler.add_user(user_data)
        logger.info(f'Add user {user_id}')

        return jsonify({'user_id': user_id}), 200

    @app.route(f'{USERS_ENDPOINT}/<string:user_id>', methods=['PUT'])
    @request_schema(PatchUserSchema())
    def update_user_info(user_id):
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        user_data = request.get_json()
        logger.info(f'Received update_user_info request: {user_data} for user {user_id}')
        upd_profile = users_handler.update_user_info(user_id, user_data)

        return jsonify(upd_profile), 200

    @app.route(f'{USERS_ENDPOINT}/<string:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        logger.info(f'Received delete_user request for user: {user_id}')
        users_handler.delete_user(user_id)
        return f'User {user_id} was deleted', 200

    @app.route(f'{USER_STATS_ENDPOINT}/<string:user_id>', methods=['GET'])
    def access_user_stats(user_id):
        logger.info(f'Received access_user_stats request for user: {user_id}')
        return send_file(f'{USER_STATS_DIR}/{user_id}.pdf')

    @app.route(f'{USER_STATS_ENDPOINT}/<string:user_id>', methods=['POST'])
    @response_schema(UserStatsResponseSchema())
    def get_user_stats(user_id):
        logger.info(f'Recieved get_user_stats request for id: {user_id}')
        users_handler.get_stats(user_id)
        stats_url = f'{BASE_URL}{USER_STATS_ENDPOINT}/{user_id}'
        logger.info(f'User {user_id} stats: {stats_url}')

        return jsonify({'url': stats_url}), 200

    @app.route(f'{GAMES_ENDPOINT}/<string:game_id>', methods=['GET'])
    @response_schema(GameResponseSchema())
    def get_game(game_id):
        logger.info(f'Recieved get_game request for id: {game_id}')
        game = games_handler.get_game(game_id)
        logger.info(f'Game with id {game_id}: {game}')

        return jsonify(game), 200

    @app.route(GAMES_ENDPOINT, methods=['GET'])
    @request_schema(GameIdsSchema())
    @response_schema(GameResponsesSchema())
    def get_games():
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        game_ids = request.json['game_ids']
        logger.info(f'Recieved get_games request for ids: {game_ids}')
        games = games_handler.get_games(game_ids)
        logger.info(f'Find games: {games}')

        return jsonify({'games': games}), 200

    @app.route(GAMES_ENDPOINT, methods=['POST'])
    @request_schema(AddGameSchema())
    @response_schema(AddGameResponseSchema())
    def add_game():
        if not request.is_json:
            raise BadRequest('Content-Type must be application/json')

        game_data = request.get_json()
        logger.info(f'Received add_game request: {game_data}')
        game_id = games_handler.add_game(game_data)
        logger.info(f'Add game {game_id}')

        return jsonify({'game_id': game_id}), 200

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        logger.error(error)
        return f'Bad request: {error}', 400

    @app.errorhandler(Exception)
    def handle_exception(exception):
        traceback.print_exc()
        logger.error(exception)
        return f'During processing your request error occured: {exception}', 500

    return app
