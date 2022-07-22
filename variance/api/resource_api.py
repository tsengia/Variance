
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
    class VarianceResourceCollectionEndpoint(MethodView):

        @blueprint.response(200, resource_schema(many=True))
        @blueprint.paginate()
        def get(self, pagination_parameters):
            authorize_user_or_abort(g.user, endpoint_name + ".list", False)

            # base query that we will then filter out            
            base_query = resource_model.query.all()
            
            # TODO: Apply search filters
            # TODO: Apply user-level visibility
    
            # flask-smorest needs us to set the item_count
            total_count = base_query.count()
            pagination_parameters.item_count = total_count
            
            paginate_query = base_query.paginate(
                pagination_parameters.page,
                pagination_parameters.page_size)

            return paginate_query.items

        @blueprint.arguments(resource_schema(exclude=("id",))
        @blueprint.response(200, resource_schema)
        def post(self, new_resource: resource_schema) -> resource_model:
            authorize_user_or_abort(g.user, endpoint_name + ".new", False)
            # TODO: Enforcement of unique constraints
            m = resource_model(**new_resource)
            db.session.add(m)
            db.session.commit()
            return m 

    @blueprint.route("/<int:resource_id>")
    class VarianceResourceEndpoint(MethodView):

        @blueprint.response(200, resource_schema)
        def get(self, resource_id: int) -> resource_model:
            m = resource_model.query.get_or_404(resource_id)
            authorize_user_or_abort(g.user, endpoint_name + ".view", m)
            return m

        @blueprint.arguments(resource_schema)
        @blueprint.response(200, resource_schema)
        def put(self, resource_patch: object, resource_id: int) -> resource_omdel:
            m = resource_model.query.get_or_404(resource_id)
            authorize_user_or_abort(g.user, endpoint_name + ".delete", m)
          
            # Check to make sure the user is not modifying the ID value
            if resource_id != resource_patch.id:
                abort(409, "You are not permitted to change the ID of a resource!")

            # Apply the update
            for key, value in resource_patch.items():
                setattr(m, key, value)

            # Commit the changes
            db.session.commit()
            return m 
    
        @blueprint.response(204)
        def delete(self, resource_id: int):
            m = resource_model.query.get_or_404(resource_id)
            authorize_user_or_abort(g.user, endpoint_name + ".delete", m)
            db.session.delete(m)
            db.session.commit()
            return
