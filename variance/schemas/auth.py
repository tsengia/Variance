import marshmallow as ma

class TokenAuthSchema(ma.Schema):
    token = ma.String()