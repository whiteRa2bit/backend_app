import os

import redis
from loguru import logger
from reportlab.pdfgen.canvas import Canvas
from rq import Queue

from mafia_resources.api.schema.game_schema import GameStatus
from mafia_resources.config import USER_STATS_DIR
from mafia_resources.db.users_collection import users_collection
from mafia_resources.db.games_collection import games_collection

_redis_instance = redis.Redis(host='redis')
_queue = Queue(connection=_redis_instance)
PDF_X = 70
PDF_Y = 800
PDF_Y_STEP = 50


def object_id_to_user_id(user):
    user['user_id'] = user.pop(users_collection.id_field_name)
    user['user_id'] = str(user['user_id'])
    return user


def get_user(user_id):
    user = users_collection.get_user(user_id)
    user = object_id_to_user_id(user)
    return user


def get_users(user_ids):
    users = users_collection.get_users(user_ids)
    users = list(map(object_id_to_user_id, users))
    return users


def add_user(user_data):
    user_id = users_collection.add_user(user_data)
    return str(user_id)


def update_user_info(user_id, user_data):
    upd_profile = users_collection.update_user(user_id, user_data)
    return upd_profile


def delete_user(user_id):
    return users_collection.delete_user(user_id)


def _get_stats_backround(user_id):
    user = users_collection.get_user(user_id)
    user = object_id_to_user_id(user)
    logger.info(f'Processing user: {user}')
    games = []
    if 'game_ids' in user:
        for game_id in user['game_ids']:
            games.append(games_collection.get_game(game_id))
        logger.info(f'Games for user {user_id}: {games}')

    pdf_strings = [f'{field}: {user[field]}' for field in user if field != 'game_ids']
    pdf_strings.append(f'Games number: {len(games)}')
    pdf_strings.append(f'Wins number: {len([game for game in games if game["status"] == GameStatus.win.value])}')
    pdf_strings.append(f'Loses number: {len([game for game in games if game["status"] == GameStatus.lose.value])}')
    pdf_strings.append(f'Total play time: {sum([game["length"] for game in games])}')

    canvas = Canvas(os.path.join(USER_STATS_DIR, f'{user_id}.pdf'))
    pdf_y = PDF_Y
    for pdf_string in pdf_strings:
        canvas.drawString(PDF_X, pdf_y, pdf_string)
        pdf_y -= PDF_Y_STEP
    canvas.save()


def get_stats(user_id):
    job = _queue.enqueue(_get_stats_backround, user_id)
    logger.info(f"Task ({job.id}) added to queue at {job.enqueued_at}")
