from marshmallow import fields, Schema, ValidationError, validates
from flask_smorest import abort
import re

# Regex used to check if a username is legal or not.
# Usernames can contain any lower or uppercase letters and numbers.
# Usernames must be between 3 and 21 charecters long.
username_regex = re.compile("^[a-zA-Z0-9_-]{3,21}$")

class TokenAuthSchema(Schema):
    token = fields.String()


class RegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    birthdate = fields.Date(required=True)

    @validates("username")
    def validate_new_username(self, value):
        # Make sure there are no illegal characters, meets length requirements, and is unique.
        if not username_regex.match(value):
            abort(422, message="Username must be between 3 and 21 characters and can only contain alphanumeric values!")

    @validates("password")
    def validate_new_password(self, value):
        if len(value) < 8:
            abort(422, message="Password must be at least 8 characters long!")


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates("username")
    def validate_username(self, value):
        # By double checking that the username is legal, we save ourselves a hit to the database.
        if not username_regex.match(value):
            abort(422, message="Username must be between 3 and 21 characters and can only contain alphanumeric values!")

    @validates("password")
    def validate_password(self, value):
        # By checking the length of the password, we save ourselve a hit to the database.
        if len(value) < 8:
            abort(422, message="Password must be at least 8 characters long!")
