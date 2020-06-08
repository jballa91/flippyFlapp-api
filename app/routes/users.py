from flask import Blueprint, jsonify
from flask_cors import cross_origin
from ..auth import requires_auth

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/<int:user_id>")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_user():
    body = request.json
    user = User.query.filter_by(email=body["email"]).first()
    return jsonify({"userId": user.id,
                    "email": user.email,
                    "nickname": user.nickname,
                    "name": user.name})


@bp.route("/<int:user_id>", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def post_user():
    body = request.json
    user_db = User.query.filter_by(email=body["email"]).first()
    if user_db:
        user_db.nickname = body["nickname"]
        user_db.name = body["name"]
        return jsonify({"userId": user_db.id}, 201)
    else:
        new_user = User(email=body["email"],
                        nickname=body["nickname"],
                        name=body["name"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user, 201)
