import json
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from RAG.rag import run_qa_chain_with_context
from evaluation._data_generation import main
from evaluation._data_generation import file_reader
from evaluation._evaluation import evaluate
from script.save_to_json import save_json_to_file
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Initialize Flask app
main_app = Blueprint('main', __name__)
CORS(main_app, resources={r"/*": {"origins": "*"}})


# Route for handling user messages
@main_app.get('/')
def home():
    return 'welcome to promptly api '


@main_app.post('/api/chatbot')
async def chatbot():
    try:
        data = request.get_json()
        user_objective = data.get("objective", "")  # Adjust the key based on your actual data structure
        result = await run_qa_chain_with_context(user_objective)

        if result is not None:
            return jsonify({"answer": result}), 200
        else:
            return jsonify({"error": "Failed to retrieve answer."}), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

@main_app.post('/api/generated')
async def generate_prompts():
    try:
        # Assuming you're sending a JSON payload with 'num_test_output'
        data = request.get_json()
        num_test_output = data.get("num_test_output", 1)  # Default to 1 if not provided
        # Generate test data
        test_data = await main(num_test_output)
        file_path = "dataset/test-data.json"
        response = read_json_file(file_path)

        # Extract "user" from each entry
        users_only = [entry.get("user", "") for entry in response]

        # Return the "user" data as the response
        return jsonify(users_only[:num_test_output]), 200


    except Exception as e:
        return jsonify({"status": "error", "message": f"An unexpected error occurred: {e}"}), 500

@main_app.post('/api/evaluate')
async def evaluate_prompt():
    try:
        # Assuming the JSON payload has a 'user_message' key
        data = request.get_json()
        user_message = data.get('user_message',"")

        # Fetch other required data (context, prompt) as needed
        context_message = file_reader("prompts/context.txt")
        prompt_message = file_reader("prompts/generic-evaluation-prompt.txt")
        context = str(context_message)
        prompt = str(prompt_message)

        # Evaluate and save to JSON file
        response = await evaluate(prompt, user_message, context)
        save_json_to_file({'prompt': user_message, 'response': response})

        return jsonify({'prompt': user_message, 'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_app.get('/api/get_prompts')
def get_prompts():
    try:
        # Read the prompts from the JSON file
        with open('prompt_generated/prompts.json', 'r') as json_file:
            prompts = json.load(json_file)

        return jsonify(prompts), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
