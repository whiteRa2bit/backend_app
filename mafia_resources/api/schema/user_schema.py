from enum import Enum, unique

import bson
from marshmallow import Schema, validates, ValidationError
from marshmallow.fields import List, Email, Str, URL, Nested
from marshmallow.validate import Length, OneOf


@unique
class Gender(Enum):
    female = 'female'
    male = 'male'


class PatchUserSchema(Schema):
    username = Str(validate=Length(min=1, max=256))
    gender = Str(validate=OneOf([gender.value for gender in Gender]))
    email = Email()
    avatar_url = URL()
    game_ids = List(Str())


class UserSchema(PatchUserSchema):
    user_id = Str(required=True)
    username = Str(validate=Length(min=1, max=256), required=True)
    gender = Str(validate=OneOf([gender.value for gender in Gender]))
    email = Email()
    avatar_url = URL()
    game_ids = List(Str())

    @validates('user_id')
    def validate_user_id(self, user_id):
        if not bson.ObjectId.is_valid(user_id):
            raise ValidationError(f'{user_id} is not a valid ObjectId')

    @validates('game_ids')
    def validate_game_ids(self, game_ids):
        for game_id in game_ids:
            if not bson.ObjectId.is_valid(game_id):
                raise ValidationError(f'{game_id} is not a valid ObjectId')


class UserResponseSchema(UserSchema):
    pass


class UsersResponseSchema(Schema):
    users = Nested(UserSchema(many=True), required=True)


class UserIdSchema(Schema):
    user_id = Str(required=True)

    @validates('user_id')
    def validate_user_id(self, user_id):
        return bson.ObjectId.is_valid(user_id)


class UserIdsSchema(Schema):
    user_ids = List(Str(), required=True)

    @validates('user_ids')
    def validate_user_ids(self, user_ids: list):
        for user_id in user_ids:
            if not bson.ObjectId.is_valid(user_id):
                raise ValidationError(f'{user_id} is not a valid ObjectId')
        if len(user_ids) != len(set(user_ids)):
            raise ValidationError('user ids must be unique')


class AddUserSchema(PatchUserSchema):
    username = Str(validate=Length(min=1, max=256), required=True)


class AddUserResponseSchema(UserIdSchema):
    pass


class UserStatsResponseSchema(Schema):
    url = URL()
