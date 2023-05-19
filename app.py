import streamlit as st
import speech_recognition as sr
import webbrowser
import openai 
import datetime
import random
import numpy as np 
import yfinance as yf

chatStr = ""

def chat(query):
    global chatStr
    openai.api_key = "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"
    chatStr += f"Gaurang: {query}\n AI-Bot: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_text = response["choices"][0]["text"]
    chatStr += f"{response_text}\n"
    st.text_area('AI-Bot:', value=response_text)
    return response_text

def ai(prompt):
    openai.api_key = "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"
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)
    
    return response["choices"][0]["text"]

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            st.text("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            st.text(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from AI-Bot"

def main():
    st.set_page_config(layout="wide")

    # Initialize chatStr
    global chatStr
    chatStr = ""

    # Set A.I-Bot in the middle of the web page in green color
    st.markdown(
        "<h1 style='text-align: center; color: green;'>AI-Bot (Portfolio Management Integrated)</h1>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown("Basic Commands  for the Bot")
    st.sidebar.markdown("1. Open Youtube")
    st.sidebar.markdown("2. Open Wikipedia")
    st.sidebar.markdown("3. Open Google")
    st.sidebar.markdown("4. Open AI Answering - Ask any question just start with 'TM:'")
    st.sidebar.markdown("4. AI Bot Quit - To quit the bot")
    st.sidebar.markdown("5. Reset Chat - To start a new conversation")
    st.sidebar.markdown("6. Managed Portfolio - Based on Monthly returns")


    # User input box and buttons in a single row
    user_input_col, send_col, speak_col = st.columns([10, 1, 1])

    query = user_input_col.text_input('User:')
    if send_col.button('Send'):
        if query:

            response = ""
            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    response = "Opening requested website sir..."
                    st.write(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])

        if "TM:".lower() in query.lower():
            response = ai(prompt=query)
            st.write(response)

        elif "AI Bot Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        elif "managed portfolio".lower() in query.lower():

            stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "HINDUNILVR.NS", "INFY.NS", "ICICIBANK.NS",
                      "KOTAKBANK.NS", "AXISBANK.NS", "LT.NS", "SBIN.NS", "ASIANPAINT.NS", "HCLTECH.NS",
                      "WIPRO.NS", "TECHM.NS", "BHARTIARTL.NS", "MARUTI.NS", "NESTLEIND.NS", "ONGC.NS",
                      "CIPLA.NS", "DRREDDY.NS"]
            # Replace with your desired stock symbols
            returns_dict = {}

            for stock in stocks:
                data = yf.Ticker(stock).history(period="1mo")  # Retrieve monthly data
                if len(data) > 0:
                    monthly_returns = (data["Close"][-1] - data["Close"][0]) / data["Close"][0]
                    returns_dict[stock] = monthly_returns

            if returns_dict:
                sorted_stocks = sorted(returns_dict, key=returns_dict.get, reverse=True)
                top_stocks = sorted_stocks[:10]  # Select the top 10 stocks with highest returns

                response = "The highest profitable 10 stocks in your portfolio (based on monthly returns) are:\n"
                for stock in top_stocks:
                    response += f"{stock}: {returns_dict[stock]:.2%}\n"
            else:
                response = "No stock data available."

            st.write(response)

        else:
            st.write("Chatting...")
            # response = chat(query)

        st.text_area('AI-Bot:', value=response, height=400)

    audio_query = speak_col.button("Speak")
    if audio_query:
        st.write("Speak your query...")
        query = takeCommand()
        if query:
            response = chat(query)
            st.text_area('AI-Bot:', value=response, height=400)
        
if __name__ == '__main__':
    main()
