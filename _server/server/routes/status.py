from flask import Response, request,jsonify
from flask import Blueprint


status_dp = Blueprint('status', __name__)
@app.route('/prompt', methods=['GET'])
def app_check():
  return 'ok'