
from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance.extensions import db

from variance.common.util import validate_unique_or_abort
from variance.common.authorize import check_persm_or_abort

import marshmallow
from marshmallow import EXCLUDE

class VarianceResource(resource_schema, resource_model, file_name: str, endpoint_name: str):

    blueprint = Blueprint(endpoint_name, file_name, url_prefix="/" + endpoint_name)

    self._resource_schema = resource_schema
    self._resource_model = resource_model
    self._endpoint_name = endpoint_name

    @blueprint.route("/")
    class Collection(MethodView):
        @blueprint.arguments(resource_schema())
        @blueprint.response(201, resource_schema())
        def post(self, post_schema: resource_schema) -> resource_model:
            "Endpoint for creating new instances of this type"
            authorize_user_or_abort(False, self._resource_schema + ".new", resource_model)
