from flask import Blueprint
from flask import Response, request,jsonify


users_bp = Blueprint('users', __name__, url_prefix='/users')
@users_bp.route('', methods=['GET'])
def get_all_telegram_users():
  users = db.session.sca
  return jsonify(all_users)


@users_bp.route('', method=["POST"])
def create_user():
  d = request.json
  print(d)
  return Response(status=200)
  return jsonify(d), 201