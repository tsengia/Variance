from typing import Type

from flask import g
from flask.views import MethodView
import flask_smorest

from variance.extensions import db, ResourceBase

from variance.common.util import validate_unique_or_abort
from variance.common.authorize import authorize_user_or_abort

import marshmallow
from marshmallow import EXCLUDE
from uuid import UUID

class VarianceCollection():
    "Implements a standard CRUD endpoint for the given DB Model."    

    def attach(self, api, url_prefix: str):
        "Attaches the endpoint to the provided smoREST API object"
        api.register_blueprint(self.blueprint, url_prefix=url_prefix + self._endpoint_name)

    def __init__(self, resource_model: Type[ResourceBase], 
                resource_schema: Type[marshmallow.Schema], 
                file_name: str, endpoint_name: str,
                ):
        """
        Create a new VarianceResource endpoint.
        """
        self._resource_schema = resource_schema
        self._resource_model = resource_model
        self._endpoint_name = endpoint_name
        
        self.blueprint = flask_smorest.Blueprint(endpoint_name, file_name, 
                                    url_prefix="/" + endpoint_name)


        @self.blueprint.route("/", methods=["GET"])
        @self.blueprint.etag
        @self.blueprint.response(200, resource_schema(many=True))
        def resource_list_get():
            authorize_user_or_abort(g.user, f"{endpoint_name}.list", False)
            # base query that we will then filter out            
            base_query = db.session.query(resource_model)
            
            # TODO: Apply search filters
            # TODO: Apply user-level visibility
            # TODO: Pagination?

            # flask-smorest needs us to set the item_count
            #total_count = base_query.count()
            #pagination_parameters.item_count = total_count
            
            #paginate_query = base_query.paginate(
            #    pagination_parameters.page,
            #    pagination_parameters.page_size)

            #return paginate_query.items
            return base_query

        self.resource_list_get = resource_list_get

        @self.blueprint.route("/", methods=["POST"])
        @self.blueprint.arguments(resource_schema)
        @self.blueprint.response(200, resource_schema)
        def resource_list_post(new_resource: resource_schema) -> resource_model:
            authorize_user_or_abort(g.user, "{endpoint_name}.new", False)

            m = resource_model(**new_resource)
            db.session.add(m)
            db.session.commit()
            return m 

        self.resource_list_post = resource_list_post

        @self.blueprint.route("/<uuid:resource_uuid>", methods=["GET"])
        @self.blueprint.etag
        @self.blueprint.response(200, resource_schema)
        def resource_get(resource_uuid: UUID) -> resource_model:
            resource_uuid = str(resource_uuid)
            m = resource_model.query.get_or_404(resource_uuid)
            authorize_user_or_abort(g.user, f"{endpoint_name}.view", m)
            return m

        self.resource_get = resource_get

        @self.blueprint.route("/<uuid:resource_uuid>", methods=["PUT"])
        @self.blueprint.etag
        @self.blueprint.arguments(resource_schema)
        @self.blueprint.response(200, resource_schema)
        def resource_put(resource_patch: object, resource_uuid: UUID) -> resource_model:
            resource_uuid = str(resource_uuid)
            m = resource_model.query.get_or_404(resource_uuid)
            authorize_user_or_abort(g.user, f"{endpoint_name}.update", m)

            # Apply the update
            for key, value in resource_patch.items():
                setattr(m, key, value)

            # Commit the changes
            db.session.commit()
            return m 

        self.resource_put = resource_put
 
        @self.blueprint.route("/<uuid:resource_uuid>", methods=["DELETE"])
        @self.blueprint.etag
        @self.blueprint.response(204)
        def resource_delete(resource_uuid: UUID):
            resource_uuid = str(resource_uuid)
            m = resource_model.query.get_or_404(resource_uuid)
            authorize_user_or_abort(g.user, f"{endpoint_name}.delete", m)
            db.session.delete(m)
            db.session.commit()
            return

        self.resource_delete = resource_delete

class VarianceChildResource():
    "Implements a standard CRUD endpoint for the given DB Model that has a parent model."    

    def attach(self, api, url_prefix: str):
        "Attaches the endpoint to the provided smoREST API object"
        api.register_blueprint(self.blueprint, url_prefix=url_prefix + self._endpoint_name)

    def __init__(self, 
                resource_model: Type[ResourceBase], 
                resource_schema: Type[marshmallow.Schema], 
                file_name: str, endpoint_name: str,
                parent: VarianceCollection,
                ):
        """
        Create a new VarianceResource endpoint.
        """
        self._resource_schema = resource_schema
        self._resource_model = resource_model
        
        parent_model = parent._resource_model
        parent_endpoint = parent._endpoint_name
        self._endpoint_name = f"{parent_endpoint}"
        
        self.blueprint = flask_smorest.Blueprint(endpoint_name, file_name, 
                                    url_prefix="/" + self._endpoint_name)

        @self.blueprint.route(f"/<uuid:parent_uuid>/{endpoint_name}/", methods=["GET"])
        @self.blueprint.etag
        @self.blueprint.response(200, resource_schema(many=True))
        def resource_get(parent_uuid: UUID) -> resource_model:
            parent_uuid = str(parent_uuid)
            p = parent_model.query.get_or_404(parent_uuid)
            m = getattr(p, endpoint_name)
            authorize_user_or_abort(g.user, f"{parent_endpoint}.{endpoint_name}.view", m)
            return m

        self.resource_list_get = resource_get

        @self.blueprint.route(f"/<uuid:parent_uuid>/{endpoint_name}/", methods=["POST"])
        @self.blueprint.arguments(resource_schema)
        @self.blueprint.response(200, resource_schema)
        def resource_list_post(new_resource: resource_schema, parent_uuid: UUID) -> resource_model:
            parent_uuid = str(parent_uuid)
            p = parent_model.query.get_or_404(parent_uuid)
            authorize_user_or_abort(g.user, f"{parent_endpoint}.{endpoint_name}.new", p)

            m = resource_model(**new_resource)
            getattr(p, endpoint_name).append(m)
            db.session.add(m)
            db.session.add(p)
            db.session.commit()
            return m 

        self.resource_list_post = resource_list_post

        # @self.blueprint.route(f"/<uuid:parent_uuid>/{endpoint_name}/<uuid:child_uuid>", methods=["PUT"])
        # @self.blueprint.etag
        # @self.blueprint.arguments(resource_schema)
        # @self.blueprint.response(200, resource_schema)
        # def resource_put(resource_patch: object, resource_uuid: UUID) -> resource_model:
        #     resource_uuid = str(resource_uuid)
        #     m = resource_model.query.get_or_404(resource_uuid)
        #     authorize_user_or_abort(g.user, endpoint_name + ".update", m)

        #     # Apply the update
        #     for key, value in resource_patch.items():
        #         setattr(m, key, value)

        #     # Commit the changes
        #     db.session.commit()
        #     return m 

        # self.resource_put = resource_put
 
        # @self.blueprint.route("/<uuid:resource_uuid>", methods=["DELETE"])
        # @self.blueprint.etag
        # @self.blueprint.response(204)
        # def resource_delete(resource_uuid: UUID):
        #     resource_uuid = str(resource_uuid)
        #     m = resource_model.query.get_or_404(resource_uuid)
        #     authorize_user_or_abort(g.user, endpoint_name + ".delete", m)
        #     db.session.delete(m)
        #     db.session.commit()
        #     return

        # self.resource_delete = resource_delete