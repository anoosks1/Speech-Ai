from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API with your API key
api_key = 'AIzaSyDG4tJeWI75berlhOgsoQmWfazAGuYpzAY'  # Replace with your actual API key
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash') # Or 'gemini-pro-vision' for multimodal

# Function to process the message with Gemini
def process_with_gemini(message):
    try:
        # Use the generate_content method to get the response
        response = model.generate_content(message)
        return response.text.strip() if response and hasattr(response, 'text') else "No valid response from Gemini."
    except Exception as e:
        return f"Error during Gemini processing: {str(e)}"

@app.route('/ask', methods=['POST'])
def ask():
    # Get the message from the incoming request
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({"error": "No message received"}), 400

    # Process the message (this is where Gemini API is called)
    reply = process_with_gemini(message)

    # Return the response as JSON
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)