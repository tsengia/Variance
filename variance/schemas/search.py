import marshmallow as ma


class SearchSchema(ma.Schema):
    count = ma.fields.Integer(required=False, validate=ma.validate.Range(
        0, 225), default=99999, missing=99999)
    offset = ma.fields.Integer(
        required=False, validate=ma.validate.Range(0, 255), default=0, missing=0)

    class Meta():
        unknown = ma.EXCLUDE
