from enum import Enum, unique

import bson
from marshmallow import Schema, validates, ValidationError
from marshmallow.fields import Int, List, Str, Nested
from marshmallow.validate import OneOf, Range


@unique
class GameStatus(Enum):
    win = 'win'
    lose = 'lose'


class PatchGameSchema(Schema):
    length = Int(validate=Range(min=0), strict=True, required=True)
    status = Str(validate=OneOf([status.value for status in GameStatus]), required=True)


class GameSchema(PatchGameSchema):
    game_id = Str(required=True)

    @validates('game_id')
    def validate_game_id(self, game_id):
        if not bson.ObjectId.is_valid(game_id):
            raise ValidationError(f'{game_id} is not a valid ObjectId')


class GameResponseSchema(GameSchema):
    pass


class GameResponsesSchema(Schema):
    games = Nested(GameSchema(many=True), required=True)


class GameIdSchema(Schema):
    game_id = Str(required=True)

    @validates('game_id')
    def validate_game_id(self, game_id):
        if not bson.ObjectId.is_valid(game_id):
            raise ValidationError(f'{game_id} is not a valid ObjectId')


class GameIdsSchema(Schema):
    game_ids = List(Str(), required=True)

    @validates('game_ids')
    def validate_game_ids(self, game_ids: list):
        for game_id in game_ids:
            if not bson.ObjectId.is_valid(game_id):
                raise ValidationError(f'{game_id} is not a valid ObjectId')
        if len(game_ids) != len(set(game_ids)):
            raise ValidationError('game ids must be unique')


class AddGameSchema(PatchGameSchema):
    pass


class AddGameResponseSchema(GameIdSchema):
    pass
