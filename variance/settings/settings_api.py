from typing import Type
from uuid import UUID

from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance.extensions import db, ResourceBase

from variance.common.util import validate_unique_or_abort
from variance.common.authorize import authorize_user_or_abort

from variance.settings.global_settings import get_global_setting, set_global_setting, global_settings_keys

import marshmallow
from marshmallow import EXCLUDE, Schema, fields

bp = Blueprint("settings", __name__, url_prefix="/api/settings")

class SettingsSchema(Schema):
    key = fields.Str()
    type_hint = fields.Str(dump_only=True)
    value = fields.Str()

class GlobalSettingsAPI(MethodView):
    "API Endpoint for getting and setting key-values for global settings"

    @bp.route("/global", methods=["GET"])
    @bp.etag
    @bp.response(200, SettingsSchema(many=True))
    def get(self, key):
        authorize_user_or_abort(g.user, "global_settings.view", False)
        settings = []
        for s in global_settings_keys:
            # TODO: This for loop could definitely be optimized a lot better via SQL
            settings[s] = SettingsSchema(key=s,\
                type_hint=global_settings_keys[s],\
                value=get_global_setting(s))
        return settings

    @bp.route("/global/<string:key>", methods=["GET"])
    @bp.etag
    @bp.response(200, SettingsSchema)
    def get(self, key):
        authorize_user_or_abort(g.user, "global_settings.view", False)
        return SettingsSchema(key=key,\
            value=get_global_setting(key),\
            type_hint=global_settings_keys[key])

    @bp.route("/global/<string:key>", methods=["POST", "PUT"])
    @bp.etag
    @bp.arguments(str)
    @bp.response(200, SettingsSchema)
    def update(self, key: str, value: str):
        authorize_user_or_abort(g.user, "global_settings.update", False)
        if key not in global_settings_keys:
            abort(404, message={\
                    "error": 'Global setting "{0}" not found!'.format(key)\
                })

        if set_global_setting(key, value):
            return SettingsSchema(key=key,\
                value=get_global_setting(key),\
                type_hint=global_settings_keys[key])
        else:
            abort(500, message={\
                    "error":'Failed to set global setting "{0}"'.format(key)\
                })
