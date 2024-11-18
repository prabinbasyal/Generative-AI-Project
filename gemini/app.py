# Step 1: Import the google.generativeai module and streamlit
import streamlit as st
import google.generativeai as ai

# Step 2: Configure the API key (do not hard-code API keys in production)
api_key = ""
ai.configure(api_key=api_key)

# Step 3: Initialize the LLM
model_id = "models/gemini-1.5-flash"
llm = ai.GenerativeModel(model_id)

# Step 4: Initialize the chatbot
chatbot = llm.start_chat(history=[])

# Step 5: Take the user's input and call the chatbot
while True:
    user_prompt = input("Enter the query: ")
    response = chatbot.send_message(user_prompt)
    print(response.text)
