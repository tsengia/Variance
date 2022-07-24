from typing import Type

from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance.extensions import db

from variance.common.util import validate_unique_or_abort
from variance.common.authorize import authorize_user_or_abort

import marshmallow
from marshmallow import EXCLUDE

class VarianceResource():
    
    def __init__(self, resource_model: Type[db.Model], 
                resource_schema: Type[marshmallow.Schema], 
                file_name: str, endpoint_name: str):

        self._resource_schema = resource_schema
        self._resource_model = resource_model
        self._endpoint_name = endpoint_name
        
        self.blueprint = Blueprint(endpoint_name, file_name, 
                                    url_prefix="/" + endpoint_name)


        @self.blueprint.route("/", methods=["GET"])
        @self.blueprint.response(200, resource_schema(many=True))
        @self.blueprint.paginate()
        def resource_list_get(pagination_parameters):
            authorize_user_or_abort(g.user, endpoint_name + ".list", False)

            # base query that we will then filter out            
            base_query = db.session.query(resource_model)
            
            # TODO: Apply search filters
            # TODO: Apply user-level visibility

            # flask-smorest needs us to set the item_count
            total_count = base_query.count()
            pagination_parameters.item_count = total_count
            
            paginate_query = base_query.paginate(
                pagination_parameters.page,
                pagination_parameters.page_size)

            return paginate_query.items

        @self.blueprint.route("/", methods=["POST"])
        @self.blueprint.arguments(resource_schema(exclude=("id",)))
        @self.blueprint.response(200, resource_schema)
        def resource_list_post(new_resource: resource_schema) -> resource_model:
            authorize_user_or_abort(g.user, endpoint_name + ".new", False)

            # Use metaprogramming to figure out which fields 
            #   have unique constraints
            attributes = dir(resource_model)
            fields = filter(lambda f: 
                not f.startswith('__') and not callable(getattr(obj, f)))
            for field in fields:
                if field.unique:
                    validate_unique_or_abort(
                        new_resource[field], 
                        resource_model, 
                        getattr(resource_model, field), 
                        "Unique constraint failed for " + field + "!"
                    )

            m = resource_model(**new_resource)
            db.session.add(m)
            db.session.commit()
            return m 

        @self.blueprint.route("/<int:resource_id>", methods=["GET"])
        @self.blueprint.response(200, resource_schema)
        def resource_get(resource_id: int) -> resource_model:
            m = resource_model.query.get_or_404(resource_id)
            authorize_user_or_abort(g.user, endpoint_name + ".view", m)
            return m

        @self.blueprint.route("/<int:resource_id>", methods=["PUT"])
        @self.blueprint.arguments(resource_schema)
        @self.blueprint.response(200, resource_schema)
        def resource_put(resource_patch: object, resource_id: int) -> resource_model:
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
        
        @self.blueprint.route("/<int:resource_id>", methods=["DELETE"])
        @self.blueprint.response(204)
        def resource_delete(resource_id: int):
            m = resource_model.query.get_or_404(resource_id)
            authorize_user_or_abort(g.user, endpoint_name + ".delete", m)
            db.session.delete(m)
            db.session.commit()
            return
