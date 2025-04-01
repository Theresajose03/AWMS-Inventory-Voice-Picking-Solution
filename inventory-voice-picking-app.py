import streamlit as st
import openai
import azure.cognitiveservices.speech as speechsdk
import os

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "https://awms-openai-service.openai.azure.com/"  # Example: https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY = "8j8W2DSltNH9IFdGbs8siQ3JUVRfGe1MKpYsyTA9ex3B1mII3u9NJQQJ99BDACYeBjFXJ3w3AAABACOGaheJ"
DEPLOYMENT_NAME = "awms-gpt-35-turbo-deployment"  # Name of your GPT-3.5 Turbo deployment

# Azure Speech Service Configuration
SPEECH_KEY = "3K7qKIHTuKTsyA9AdilW776365lU8lp8e9FQxgra8d47amHKu4ceJQQJ99BCACGhslBXJ3w3AAAYACOGYd7q"
SPEECH_REGION = "centralindia"

def recognize_speech():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    st.write("🎤 Listening...")
    result = speech_recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return ""

def ask_openai(question):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    
    data = {
        "messages": [{"role": "user", "content": question}],
        "model": DEPLOYMENT_NAME
    }
    
    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=data["messages"],
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("📦 AWMS - Voice Picking System")

name = st.text_input("👤 Enter your name")
if name:
    st.markdown(f"👋 Welcome, {name}!")

col1, col2 = st.columns(2)

# Warehouse Inventory Q&A Section
with col1:
    st.subheader("🔍 Ask Anything About Warehouse Inventory")
    user_query = st.text_input("Enter your question")
    if st.button("🎤 Speak"):
        user_query = recognize_speech()
        st.text_input("Recognized Speech", user_query)
    
    if user_query:
        answer = ask_openai(user_query)
        st.write("🤖", answer)

# Stock Check Section with Voice Input
with col2:
    st.subheader("📊 Check Stock Details")
    stock_query = st.text_input("Enter Product ID or Product Name")
    if st.button("🎤 Speak for Stock Search"):
        stock_query = recognize_speech()
        st.text_input("Recognized Speech", stock_query)
    
    if stock_query:
        stock_info = ask_openai(f"Check stock details for {stock_query}")
        st.write("📦", stock_info)
