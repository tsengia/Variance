import datetime
import jwt
from flask import g, session, request, current_app
from flask_smorest import Blueprint, abort

from variance.extensions import db
from variance.models.user import UserModel
from variance.schemas.auth import RegisterSchema, LoginSchema
from variance.common.util import validate_unique_or_abort
from variance.common.authorize import authorize_user_or_abort

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Create new user
@bp.route("/register", methods=["POST"])
@bp.arguments(RegisterSchema, location="form")
def register(new_user):
    validate_unique_or_abort(new_user["username"], UserModel, UserModel.username, "A user with that username already exists!")
    u = UserModel(username=new_user["username"],
                  birthdate=new_user["birthdate"])
    u.set_password(new_user["password"])
    current_app.defaults_manager.populate_user_with_defaults(u)
    db.session.add(u)
    db.session.commit()
    return {"id": u.id}, 201

# User login via JWT
@bp.route("/token", methods=["POST"])
@bp.arguments(LoginSchema, location="form")
def get_token(req_user):
    u = UserModel.query.filter_by(username=req_user["username"]).first()
    if u is None:
        abort(403, message="Incorrect username or password!")
    if not u.check_password(req_user["password"]):
        abort(403, message="Incorrect username or password!")
    token = jwt.encode({"user_id": u.id, "exp": datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=60)}, current_app.config["SECRET_KEY"], algorithm="HS256")
    return {"token": token}, 200

# User login via session
@bp.route("/login", methods=["POST"])
@bp.arguments(LoginSchema, location="form")
def login(req_user):
    u = UserModel.query.filter_by(username=req_user["username"]).first()
    if u is None:
        abort(403, message="Incorrect username or password!")
    if not u.check_password(req_user["password"]):
        abort(403, message="Incorrect username or password!")
    session.clear()
    session["user_id"] = u.id
    return {"status": "You have been logged in."}, 200

# User logout via session
@bp.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return {"message": "Logged out."}

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id", None)

    if user_id is None:
        g.user = None
        token = request.values.get("token", None)
        if token is not None:
            try:
                decoded_token = jwt.decode(
                    token, current_app.config["SECRET_KEY"], algorithms="HS256")
                user_id = int(decoded_token["user_id"])
            except BaseException:
                current_app.logger.warning(
                    "User attempted to use an invalid token!")
    else:
        user_id = int(user_id)

    if user_id is not None:
        g.user = UserModel.query.get(user_id)

