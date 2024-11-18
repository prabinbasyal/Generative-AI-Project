import streamlit as st
import google.generativeai as genai

# configure the API key from GoogleAI
genai.configure(api_key ='' )

# initialize the generative model
llm = genai.GenerativeModel("models/gemini-1.5-flash")

# start a new chatbot session 
chatbot = llm.start_chat(history = [])

# streamlit UI for chatbot
st.title(" Welcome to the chatbot")

# display initial AI message 
st.chat_message("ai").write("Hi there! I am a helful AI Assistant.How can I help you today?")

# user input for the chatbot
human_prompt = st.chat_input("Say something")

if human_prompt:
    # display the human message
    st.chat_message("human").write(human_prompt)
    # send the message to the chatbot and get a reponse
    response = chatbot.send_message(human_prompt)
    # Update the chatbot's chat history with the new message and response
    chatbot.history.append({"role":"human", "content":"human_prompt"})
    chatbot.history.append({"role":"ai", "content":"response.text"})
    # Display the AI's response
    st.chat_message('ai').write(response.text)