from typing import Type
from uuid import UUID

from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance.extensions import db, ResourceBase

from variance.common.util import validate_unique_or_abort
from variance.common.authorize import authorize_user_or_abort

import marshmallow
from marshmallow import EXCLUDE, Schema, fields

bp = Blueprint("settings", __name__, url_prefix="/settings")

class SettingsSchema(Schema):
    key = fields.Str()
    type_hint = fields.Str(dump_only=True)
    value = fields.Str()

class GlobalSettingsAPI(MethodView):
    "API Endpoint for getting and setting key-values for global settings"

    @bp.route("/global/", methods=["GET"])
    @bp.route("/global/<str:key>", methods=["GET"])
    @bp.etag
    @bp.response(200, SettingsSchema)
    def get(self, key):
        if key is None:
            # Reply with all of the global settings
            return
        else:
            # Reply the value of that key
            
    @bp.route("/global/<str:key>", methods=["POST", "PUT"])
    @bp.etag
    @bp.response(200, SettingsSchema)
    def update(self, key: str, value: str)
        # TODO: authorize user
        
