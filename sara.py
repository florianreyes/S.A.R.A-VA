import speech_recognition as sr
import playsound
from gtts import gTTS
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import subprocess
import os
from stock_list import stocks
import json
import requests
import config


URL = "https://api.openweathermap.org/data/2.5/weather?"


def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # speak("i am listening")
        # print("i am listening")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
            speak("sorry sir, i couldn't hear you properly.")
    return said


def get_stocks(stock, action):
    stock_l = stock.lower()
    action_l = action.lower().split(' ')

    if stock_l in stocks:
        ticker = yf.Ticker(stocks[stock_l])
    else:
        print("Sorry, I couldn't find that stock.")
        return
    for action in action_l:
        if action == "dividends" or action == "dividend":
            df = ticker.dividends
            print(df)
            data = df.resample('Y').sum()
            data = data.reset_index()
            data['Year'] = data['Date'].dt.year
            plt.figure()
            plt.bar(data['Year'], data['Dividends'])
            plt.xlabel('Year')
            plt.ylabel('Dividend Yield ($)')
            plt.title('{} historic dividend yield'.format(stock))
            plt.xlim(2000, datetime.now().year)
            plt.show()
        elif action == "cash" or action == "cashflow":
            print(ticker.cashflow)
        elif action == "major" or action == "holders":
            print(ticker.major_holders)
        elif action == "institutional":
            print(ticker.institutional_holders)
        else:
            print("Sorry, I couldn't find that information.")

def get_weather(t):
    LOCATION = t
    data = requests.get(URL+"q="+LOCATION+"&APPID="+config.API_KEY)
    data_json = data.json()
    speak("the weather in {} is {}, the temperature is {} degrees Celsius or {} degrees Fahrenheit".format(
        LOCATION, data_json['weather'][0]['description'], round((data_json['main']['temp']-273.15), 1), round((data_json['main']['temp']-273.15)*9/5+32, 1)))
    print(data_json["main"]["temp"]-273.15)


def get_note(note):
    speak("how would you like to name your note, sir?")
    file_name = get_audio()+".txt"
    with open(file_name, "w") as f:
        f.write(note)
    subprocess.run(['open', file_name], capture_output=True, text=True)
    speak("Note saved as " + file_name)


WAKE = ["hey sara", "okay sara", "hi sara", "hello sara",
        "sara", "there", "are", "you", "listen"]

while True:
    text = get_audio().lower()
    if any(word in text for word in WAKE):
        speak("Hello sir, I am ready")
        text = get_audio().lower()

        NOTE_WORDS = ["note", "make a note",
                      "make a note of this", "write this down", "write down"]
        for word in NOTE_WORDS:
            if word in text:
                speak("What would you like to note, sir?")
                note = get_audio()
                get_note(note)
                speak("Done, sir.")
                break

        STOCK_WORDS = ["stock", "stuck","stalk", "stocks", "market",
                       "market data", "stock info", "stock data"]
        for word in STOCK_WORDS:
            if word in text:
                speak("What stock would you like to know about, sir?")
                stock = get_audio()
                speak("What would you like to know about the stock, sir? Please say dividends, cash, major holders, or institutional holders.")
                action = get_audio()
                get_stocks(stock, action)
                speak("Done, sir.")
                break

        WEATHER_WORDS = ["how cold is it", "cold",
                         "hot", "weather", "temperature"]
        for word in WEATHER_WORDS:
            if word in text:
                speak(
                    "What location would you like to know the weather in, sir? Please say the city name.")
                city = get_audio()
                try:
                    get_weather(city)
                except:
                    speak(
                        "Sorry, sir. I couldn't find the weather in that location. Please repeat the city.")
                speak("Done, sir.")
                break
    GOODBYE_WORDS = ["goodbye", "bye", "see you later", "see you", "later"]
    for word in GOODBYE_WORDS:
        if word in text:
            speak("Goodbye, sir.")
            exit()
