from flask import Blueprint
from flask import Response, request,jsonify


users_bp = Blueprint('/', __name__, url_prefix='/users')

@users_bp.route('/submit_data', method=["POST"])
def submit_data():
  try:
    data = request.json
    submitted_string = data.get('submitted_string', '')
    processed_result = process_string(submitted_string)
    return jsonify({'status': 'success', 'result': processed_result})
  except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({'status': 'error', 'message': str(e)}), 500
 
def process_string(submitted_string):
    # updated later
    return submitted_string.upper()