from marshmallow import fields, ValidationError, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from variance.models.user import UserModel

import re

# Regex used to check if a username is legal or not.
# Usernames can contain any lower or uppercase letters and numbers.
# Usernames must be between 3 and 21 charecters long.
username_regex = re.compile("^[a-zA-Z0-9_-]{3,21}$")

class UserSchema(SQLAlchemyAutoSchema):
    """
    User schema that contains everything about a user.
    Note: Bad idea to expose all of this on an API endpoint.
    """
    class Meta:
        model = UserModel
        load_instance = False

class PublicProfileSchema(Schema):
    """
    Information that is always publically viewable.
    """
    username = fields.String(required=True)
    created_on = fields.DateTime(required=True)
    role = fields.String(required=True)

class PrivateProfileSchema(Schema):
    """
    Information that is always viewable by the user themselves.
    """
    username = fields.String(required=True)
    email = fields.Email(required=True)
    birthdate = fields.Date(required=True)
    created_on = fields.DateTime(required=True)
    role = fields.String(required=True)

class UserDietSchema(Schema):
    """
    Information about a user's dietary restrictions
    """
    no_peanuts = fields.Boolean()
    no_treenuts = fields.Boolean()
    no_dairy = fields.Boolean()
    no_eggs = fields.Boolean()
    no_pork = fields.Boolean()
    no_beef = fields.Boolean()
    no_meat = fields.Boolean()
    no_fish = fields.Boolean()
    no_shellfish = fields.Boolean()
    no_gluten = fields.Boolean()
    is_vegetarian = fields.Boolean()
    is_vegan = fields.Boolean()
    is_kosher = fields.Boolean()

class UserSettingsSchema(Schema):
    """
    Personalized settings for the user.
    """
    exercise_weight_unit_id = fields.Integer(required=True)
    exercise_distance_unit_id = fields.Integer(required=True)
    food_weight_unit_id = fields.Integer(required=True)
    food_volume_unit_id = fields.Integer(required=True)
    body_weight_unit_id = fields.Integer(required=True)
    body_distance_large_unit_id = fields.Integer(required=True)
    body_distance_small_unit_id = fields.Integer(required=True)
