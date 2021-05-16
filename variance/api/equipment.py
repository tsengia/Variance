from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance import db
from variance.api.auth import login_required
from variance.models.equipment import EquipmentModel
from variance.schemas.equipment import EquipmentSchema
from variance.schemas.search import SearchSchema
from marshmallow import EXCLUDE

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@bp.route("/")
class EquipmentList(MethodView):
    @bp.arguments(EquipmentSchema(only=("name", "description")), location="form", unknown=EXCLUDE)
    @bp.response(EquipmentSchema(only=("id",)), code=201)
    @login_required
    def post(self, new_equipment): # Create a new equipment
        if EquipmentModel.query.filter_by(name=new_equipment["name"]).first() is not None:
            abort(409, message="An equipment with that name already exists!")
        e = EquipmentModel(**new_equipment)
        db.session.add(e)
        db.session.commit()
        return e
    """
    @bp.arguments(SearchSchema(), location="query", required=False)
    @bp.arguments(EquipmentSchema(only=("dimension",),partial=("dimension",)), location="query", required=False, unknown=EXCLUDE)
    @bp.response(EquipmentSchema(many=True), code=200)
    def get(self, search_args, equipment_args): # List all equipment
        if not "dimension" in equipment_args:
            result = EquipmentModel.query.limit(search_args["count"]).offset(search_args["offset"]).all()
        else:
            result = EquipmentModel.query.filter_by(dimension=unit_args["dimension"]).limit(search_args["count"]).offset(search_args["offset"]).all()

        return result
    """

@bp.route("/<int:e_id>")
class Equipment(MethodView):

    @bp.arguments(EquipmentSchema(partial=("name", "description"), exclude=("id",)), location="form", unknown=EXCLUDE)
    @login_required
    def post(self, update, e_id): # Update an equipment
        e = EquipmentModel.query.get_or_404(e_id)

        if "name" in update and update["name"] != e.name:
            if EquipmentModel.query.filter_by(name=update["name"]).count() != 0:
                abort(409, "An equipment with that name already exists!")

        for key, value in update.items():
            setattr(e, key, value)

        db.session.commit()

        return {"status":"Equipment updated."}, 200

    @login_required
    def delete(self, e_id): # Delete a piece of equipment
        e = EquipmentModel.query.get_or_404(e_id)

        db.session.delete(e)
        db.session.commit()

        return {"status":"Equipment deleted."}, 200

    @bp.response(EquipmentSchema, code=200)
    def get(self, e_id): # Display a unit
        e = EquipmentModel.query.get_or_404(e_id)
        return e
