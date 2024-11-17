from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Route for the home page to display the form
@app.route("/")
def home():
    return render_template("index.html")  # Renders the HTML frontend

# API route to handle recipe requests
@app.route("/generate_recipe", methods=["POST"])
def generate_recipe():
    # Get ingredients from the form data
    ingredients = request.json.get("ingredients")
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    # Create prompt
    prompt = f"Generate a recipe using these ingredients: {ingredients}."

    # Set up request to Groq API
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    # Send request to Groq API
    response = requests.post(url, headers=headers, json=data)

    # Check if response is successful and return JSON
    if response.status_code == 200:
        recipe = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        return jsonify({"recipe": recipe})
    else:
        return jsonify({"error": "Failed to generate recipe", "details": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)