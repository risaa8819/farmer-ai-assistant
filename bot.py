import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# ==========================================
# 1. SETUP YOUR AI CREDENTIALS
# ==========================================
import os
import toml

# 1. Try to get the key from the environment (best for production/GitHub)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. If not found, try to load it from your local secrets.toml file
if not GROQ_API_KEY:
    try:
        # Note: This path assumes you run bot.py from the main DIGITAL TWIN FOLDER
        with open(".streamlit/secrets.toml", "r") as f:
            secrets = toml.load(f)
            GROQ_API_KEY = secrets["GROQ_API_KEY"]
    except FileNotFoundError:
        print("Error: Could not find API key.")
        GROQ_API_KEY = "YOUR_KEY_HERE" # Fallback just in case

# Read your agriculture manual for the AI context
try:
    with open("agri_manual.txt", "r") as file:
        CONTEXT = file.read()
except FileNotFoundError:
    CONTEXT = "No manual found. Please check the file path."

# ==========================================
# 2. THE AI FUNCTION
# ==========================================
def get_ai_response(user_message):
    system_prompt = f"""You are an Agricultural AI assistant. 
    Answer the user's question using ONLY the context below. 
    If you don't know the answer, say you don't know.
    
    CONTEXT: {CONTEXT}
    """
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}", 
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I am having trouble connecting to my brain right now."

# ==========================================
# 3. THE WHATSAPP WEBHOOK
# ==========================================
@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    # Get the message from WhatsApp
    incoming_msg = request.values.get('Body', '').strip()
    
    # Pass it to the AI
    ai_reply = get_ai_response(incoming_msg)
    
    # Send the AI's reply back to WhatsApp
    resp = MessagingResponse()
    resp.message(ai_reply)
    return str(resp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)