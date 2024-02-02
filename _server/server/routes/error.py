from flask import  Blueprint, jsonify

error_db = Blueprint('errors',__name__)
@error_db.app_errorhandler(Exception)
def handle_generic_exception(err):
  return jsonify({'message ': 'unknown error. Please check the logs.'}),500
@error_db.app_errorhandler(NotFound)
def handle_not_found(err):
  return jsonify({'message': 'This resource not available'}),404
