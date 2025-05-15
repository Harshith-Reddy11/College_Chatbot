from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the system prompt for the chatbot
SYSTEM_PROMPT = """
You are an AI chatbot specifically designed to assist people about CMRIT, Hyderabad. Your primary purpose is to assist users with any information regarding the college, such as courses, departments, facilities, events, location, and any other relevant queries.
Website: https://cmrithyderabad.edu.in
Key Behaviors:
----------------------
1. Topic Focus: You should only respond to queries related to CMRIT, Hyderabad. Any question outside of this scope should be politely redirected or answered with a clarifying message, such as "Sorry, I can only help with information about CMRIT, Hyderabad."
2. Data Scraping: You are capable of scraping data from official sources (like the college website) when necessary. Ensure that the data you use is up-to-date and accurate.
3. Tone: Maintain a professional and polite tone in all responses.
4. Clarity: Provide concise, clear, and informative answers to each question. If the query is too broad, request more specific details.
5. Handling Unknown Queries:For questions outside of the college domain or information you don't have, reply with: "Sorry, I don't have information on that. Please ask about CMRIT, Hyderabad."
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Create a chat session with the system prompt
        chat_session = model.start_chat(history=[
            {"role": "user", "parts": [SYSTEM_PROMPT]},
            {"role": "model", "parts": ["Understood! How can I assist you today?"]}])

        # Send user message to Gemini API
        response = chat_session.send_message(user_message)
        bot_response = response.text

        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)