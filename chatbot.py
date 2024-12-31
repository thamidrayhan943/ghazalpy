# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Replace with your Google Gemini API key
GEMINI_API_KEY = 'AIzaSyAE5MI1yJ48TCpiPOi0pTEE1iyHThkKtes'
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={}".format(GEMINI_API_KEY)

# Function to load responses from a text file
def load_responses(filename):
    responses = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split(': ', 1)
            responses[key] = value
    return responses

# Load responses
responses = load_responses('responses.txt')

# Function to generate a response
def generate_response(prompt):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        try:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']

            # Use predefined responses if the prompt matches
            if "name" in prompt.lower():
                return responses['name']
            elif "who made you" in prompt.lower():
                return responses['creator']
            elif "game" in prompt.lower() and "make" in prompt.lower():
                return responses['game']
            elif "hello" in prompt.lower() or "hi" in prompt.lower():
                return responses['greeting']
            else:
                return generated_text
        except KeyError:
            return "Error: Unexpected response format."
    else:
        return "Error: Unable to generate a response."

# Define the chat route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('text', '')
    if not user_input:
        return jsonify({'reply': 'Error: No input text provided.'})

    response = generate_response(user_input)
    return jsonify({'reply': response})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
