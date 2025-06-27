import speech_recognition as sr
import requests
import pickle
import os
import time

import sounddevice as sd
import numpy as np
import io
import soundfile as sf
import pyttsx3
import requests
import pickle
import os
import time

engine = pyttsx3.init()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source, phrase_time_limit=3)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        print("Could not request results.")
        return None

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait() # Blocking call in the main thread


# Send message to Gemini AI (using API key)
# Send message to Gemini AI (using API key)
def send_to_gemini(message, api_key):

    url = "http://127.0.0.1:5000/ask"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    session_data = load_session()

    full_prompt = ""
    for entry in session_data:
        role = entry.get("role")
        msg = entry.get("message")
        if role and msg:
            full_prompt += f"{role}: {msg}\n"
    full_prompt += f"user: {message}"

    payload = {
        'message': full_prompt
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get('reply', 'No reply found in response.')
    except requests.exceptions.RequestException:
        return "Error: Could not connect to Gemini API"


# Load session data (chat history)
def load_session():
    if os.path.exists("session.pkl"):
        with open("session.pkl", "rb") as f:
            return pickle.load(f)
    return []

# Save session data (chat history)
def save_session(session_data):
    with open("session.pkl", "wb") as f:
        pickle.dump(session_data, f)

# Main function for the app

def main():
    chat_history = load_session()  # Load previous session

    while True:
        # Capture speech from user
        user_input = speech_to_text()
        if user_input:
            time.sleep(0.5)

        if user_input is None:
            continue

        # Add user input to chat history
        chat_history.append({"role": "user", "message": user_input})

        # Send the conversation to Gemini AI and get the reply
        api_key = "AIzaSyDG4tJeWI75berlhOgsoQmWfazAGuYpzAY"  # Ensure your API key is correctly set
        gemini_reply = send_to_gemini(chat_history, api_key)

        # Add Gemini reply to chat history
        chat_history.append({"role": "gemini", "message": gemini_reply})

        print(f"\033[91m{gemini_reply}\033[0m")

        # Output the reply via text to speech (blocking in the main thread)
        text_to_speech(gemini_reply)

        # Save the current session data
        save_session(chat_history)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
