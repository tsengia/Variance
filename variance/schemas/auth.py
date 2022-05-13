from marshmallow import fields, Schema, ValidationError

class TokenAuthSchema(Schema):
    token = fields.String()

def validate_usename(username):
    """
    This helper function simply checks that the username meets all legal username critera.
    Does NOT check to see if the username is registered.
    """
    
    if len(username) < 4 || len(username) > 20:
        return False

    return True

class RegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    birthdate = fields.Date(required=True)

    @validates("username")
    def validate_new_username(self, value):
        # Make sure there are no illegal characters, meets length requirements, and is unique.
        pass

    @validates("password")
    def validate_new_password(self, value):
        # Make sure it meets all password strength requirements.
        pass

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
