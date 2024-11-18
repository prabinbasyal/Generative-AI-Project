# Step 1: Import the google.generativeai module and streamlit
import streamlit as st
import google.generativeai as genai

# Step 2: Configure the API key (do not hard-code API keys in production)
api_key = ""
genai.configure(api_key= api_key)

sys_prompt = """You are a helful AI Tutor for Data Science.
Students will ask ou doubts related to various topic in data science.
Make sure to take examples while explaining a concept.
In case if a student ask any question outside the data science scope,
politely decline and tell tthem to ask the question from data science domain only."""

model = genai.GenerativeModel(model_name = "models/gemini-1.5-flash",system_instruction = sys_prompt)

st.title("Data Science Tuter Application")
user_prompt = st.text_input("Enter your query:", placeholder= "Type your query here...")
#st.title("Hello :blue[World]!")

btn_click = st.button("generate Answer")
#st.write(btn_click)

if btn_click==True:
    response = model.generate_content(user_prompt)
    st.write(response.text)