from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance.extensions import db
from variance.common.util import validation_unique_or_abort
from variance.common.authorize import check_perms_or_abort
from variance.models.unit import UnitModel
from variance.schemas.util import StatusSchema
from variance.schemas.unit import UnitSchema, UnitIDSchema
from variance.schemas.search import SearchSchema
from marshmallow import EXCLUDE

bp = Blueprint('units', __name__, url_prefix='/units')


@bp.route("/")
class UnitList(MethodView):
    @bp.arguments(UnitSchema(), location="form", unknown=EXCLUDE)
    @bp.response(201, UnitIDSchema())
    def post(self, new_unit):  # Create a new unit
        check_perms_or_abort("unit.new", False)
        if UnitModel.query.filter_by(
                name=new_unit["name"]).first() is not None:
            abort(409, message="A unit with that name already exists!")
        u = UnitModel(**new_unit)
        db.session.add(u)
        db.session.commit()
        return u

    @bp.arguments(SearchSchema(), location="query", required=False)
    @bp.arguments(UnitSchema(only=("dimension",), partial=("dimension",)),
                  location="query", required=False, unknown=EXCLUDE)
    @bp.response(200, UnitSchema(many=True))
    def get(self, search_args, unit_args):  # List all units
        check_perms_or_abort("unit.view", False)
        if "dimension" not in unit_args:
            result = UnitModel.query.limit(search_args["count"]).offset(
                search_args["offset"]).all()
        else:
            result = UnitModel.query.filter_by(
                dimension=unit_args["dimension"]).limit(
                search_args["count"]).offset(
                search_args["offset"]).all()

        return result


@bp.route("/<int:unit_id>")
class Unit(MethodView):

    @bp.arguments(UnitSchema(partial=True), location="form", unknown=EXCLUDE)
    @bp.response(200, StatusSchema)
    def post(self, update, unit_id):  # Update a unit
        u = UnitModel.query.get_or_404(unit_id)
        check_perms_or_abort("unit.update", u)
        
        if "name" in update and update["name"] != u.name:
            if UnitModel.query.filter_by(name=update["name"]).count() != 0:
                abort(409, "A unit with that name already exists!")

        for key, value in update.items():
            setattr(u, key, value)

        db.session.commit()

        return "Unit updated."

    @bp.response(200, StatusSchema)
    def delete(self, unit_id):  # Delete a unit
        u = UnitModel.query.get_or_404(unit_id)
        check_perms_or_abort("unit.delete", u)

        db.session.delete(u)
        db.session.commit()

        return "Unit deleted."

    @bp.response(200, UnitSchema)
    def get(self, unit_id):  # Display a unit
        u = UnitModel.query.get_or_404(unit_id)
        check_perms_or_abort("unit.view", u)
        return u
