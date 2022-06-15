from flask.views import MethodView
from flask_smorest import Blueprint, abort

from variance.common.authorize import check_perms_or_abort
from variance.extensions import db
from variance.models.equipment import EquipmentModel
from variance.schemas.equipment import EquipmentSchema
from variance.schemas.search import SearchSchema
from marshmallow import EXCLUDE

bp = Blueprint('equipment', __name__, url_prefix='/equipment')


@bp.route("/")
class EquipmentList(MethodView):
    @bp.arguments(EquipmentSchema(only=("name", "description")),
                  location="form", unknown=EXCLUDE)
    @bp.response(EquipmentSchema(only=("id",)), code=201)
    def post(self, new_equipment):  # Create a new equipment
        check_perms_or_abort(g.user, "equipment.create", None)
        if EquipmentModel.query.filter_by(
                name=new_equipment["name"]).first() is not None:
            abort(409, message="An equipment with that name already exists!")
        e = EquipmentModel(**new_equipment)
        db.session.add(e)
        db.session.commit()
        return e


@bp.route("/<int:e_id>")
class Equipment(MethodView):

    @bp.arguments(EquipmentSchema(partial=("name", "description"),
                  exclude=("id",)), location="form", unknown=EXCLUDE)
    def post(self, update, e_id):  # Update an equipment
        e = EquipmentModel.query.get_or_404(e_id)
        check_perms_or_abort(g.user, "equipment.update", e)
        if "name" in update and update["name"] != e.name:
            if EquipmentModel.query.filter_by(
                    name=update["name"]).count() != 0:
                abort(409, "An equipment with that name already exists!")

        for key, value in update.items():
            setattr(e, key, value)

        db.session.commit()

        return {"status": "Equipment updated."}, 200

    def delete(self, e_id):  # Delete a piece of equipment
        e = EquipmentModel.query.get_or_404(e_id)
        check_perms_or_abort(g.user, "equipment.delete", e)
        db.session.delete(e)
        db.session.commit()

        return {"status": "Equipment deleted."}, 200

    @bp.response(EquipmentSchema, code=200)
    def get(self, e_id):  # Display a unit
        e = EquipmentModel.query.get_or_404(e_id)
        check_perms_or_abort(g.user, "equipment.view", e)
        return e
