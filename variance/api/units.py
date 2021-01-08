from flask import current_app, g, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance import db
from variance.api.auth import login_required
from variance.models.unit import UnitModel
from variance.schemas.unit import UnitSchema
from variance.schemas.search import SearchSchema
from marshmallow import EXCLUDE

bp = Blueprint('units', __name__, url_prefix='/units')

@bp.route("/")
class UnitList(MethodView):
    @bp.arguments(UnitSchema(only=("name", "dimension", "abbreviation")), location="form", unknown=EXCLUDE)
    @bp.response(UnitSchema(only=("id",)), code=201)
    @login_required
    def post(self, new_unit): # Create a new unit
        if UnitModel.query.filter_by(name=new_unit["name"]).first() is not None:
            abort(409, message="A unit with that name already exists!")
        u = UnitModel(**new_unit)
        db.session.add(u)
        db.session.commit()
        return u

    @bp.arguments(SearchSchema(), location="query", required=False)
    @bp.arguments(UnitSchema(only=("dimension",),partial=("dimension",)), location="query", required=False, unknown=EXCLUDE)
    @bp.response(UnitSchema(many=True), code=200)
    def get(self, search_args, unit_args): # List all units
        if not "dimension" in unit_args:
            result = UnitModel.query.limit(search_args["count"]).offset(search_args["offset"]).all()
        else:
            result = UnitModel.query.filter_by(dimension=unit_args["dimension"]).limit(search_args["count"]).offset(search_args["offset"]).all()

        return result

@bp.route("/<int:unit_id>")
class Unit(MethodView):

    @bp.arguments(UnitSchema(partial=("name", "dimension", "abbreviation", "multiplier"), exclude=("id",)), location="form", unknown=EXCLUDE)
    @login_required
    def post(self, update, unit_id): # Update a unit
        u = UnitModel.query.get_or_404(unit_id)

        if "name" in update and update["name"] != u.name:
            if UnitModel.query.filter_by(name=update["name"]).count() is not 0:
                abort(409, "A unit with that name already exists!")

        i = UnitSchema().load(update, instance=UnitModel.query.get(unit_id), partial=True)
        db.session.commit()

        return {"status":"Unit updated."}, 200

    @login_required
    def delete(self, unit_id): # Delete a unit
        u = UnitModel.query.get_or_404(unit_id)

        db.session.delete(u)
        db.session.commit()

        return {"status":"Unit deleted."}, 200

    @bp.response(UnitSchema, code=200)
    def get(self, unit_id): # Display a unit
        u = UnitModel.query.get_or_404(unit_id)
        return u
