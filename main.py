import speech_recognition as sr
import openai
import wikipedia
import os
import webbrowser
import datetime
import requests
import pandas as pd
import json
import pyjokes
import app_paths
apps=app_paths.apps

APIKey = "9e569d36d6ec41eb84543520231011"
city="Goa"
current_weather_api_url = "http://api.weatherapi.com/v1/current.json?key="+APIKey+"&q="+city
current_response = requests.get(current_weather_api_url)
print(current_response.text)
if( current_response.status_code == 200):
    print("Api connected successfully")
elif (current_response.status_code ==201):
    print("The request was successful, but the response has no content.")
else:
    print("Error in Api connected failed")

current_data = current_response.json()
current_df = pd.json_normalize(current_data)
current_text = current_df["current.condition.text"].squeeze()
current_temp= current_df["current.temp_c"].squeeze()
current_humidity=current_df["current.humidity"]
current_windspeed=current_df["current.wind_kph"]


forecast_weather_api_url ="http://api.weatherapi.com/v1/forecast.json?key="+APIKey+"&q="+city+"&aqi=true&alerts=true&days=2"
forecast_response = requests.get(forecast_weather_api_url)
print(forecast_response.text)
if( forecast_response.status_code == 200):
    print("Api connected successfully")
elif (forecast_response.status_code ==201):
    print("The request was successful, but the response has no content.")
else:
    print("Error in Api connected failed")

forecast_data = forecast_response.json()
# forecast_df = pd.json_normalize(forecast_data)
forecast_rain = forecast_data["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"]
forecast_rain_chances=forecast_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
forecast_snow = forecast_data["forecast"]["forecastday"][0]["day"]["daily_will_it_snow"]
forecast_snow_chances=forecast_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_snow"]

forecast_rain_1 = forecast_data["forecast"]["forecastday"][1]["day"]["daily_will_it_rain"]
forecast_rain_chances_1=forecast_data["forecast"]["forecastday"][1]["day"]["daily_chance_of_rain"]
forecast_snow_1 = forecast_data["forecast"]["forecastday"][1]["day"]["daily_will_it_snow"]
forecast_snow_chances_1=forecast_data["forecast"]["forecastday"][1]["day"]["daily_chance_of_snow"]


# these keys are with 0 credits use your own, mostly now no free credits are given on new signup with openai
api_key = "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"
openai.api_key = api_key

def say(text):
    os.system(f"say {text}")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            print("audio captured!")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said:{query}")
            return query
        except Exception as e:
            return "Some error occured"

if __name__ == '__main__':
    print("raj")
    say("Hello I am Krim")
    while True:
        flag=0
        print("Listening...")
        text = takeCommand().lower()
        sites = [["youtube", "https://www.youtube.com/"], ["firefox", "https://www.firefox.com/"],
                 ["google", "https://www.google.com/"], ["wikipedia", "https://www.wikipedia.com/"]]
        for site in sites:
            if f"open {site[0]}" in text:
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                flag=1
        for app in apps:
            if f"open {app[0]}" in text:
                say(f"Opening {app[0]}")
                os.system(f"open {app[1]}")
                flag=1
        if "the time" in text:
            strfTime = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir the time is {strfTime}")
        elif "date"in text:
            say(datetime.datetime.now().strftime("%d %B %Y"))
        elif " day"in text:
            say(datetime.datetime.now().strftime("%A"))
        elif "using ai" in text:
            prompt = text.replace("using ai","")
            response = openai.Completion.create(
                engine="text-davinci-002",  # Choose the engine that fits your needs
                messages=[{"role": "ai assistant"}],
                prompt=prompt,
                max_tokens=50  # Adjust the response length as needed
            )
            translated_text = response.choices[0].text
            say(translated_text)
        elif ("search" or "what" or "who") in text:
                text = text.replace("search", "")
                text = text.replace("what", "")
                text = text.replace("who", "")
                text = text.replace("is", "")
                text = text.replace("are", "")
                ans = wikipedia.summary(text, sentences=2)
                print(ans)
                say("according to wikipedia")
                say(ans)
        elif "joke" in text:
            ans = pyjokes.get_joke()
            print(ans)
            say(ans)
        elif "rain tomorrow" in text:
            if (forecast_rain_1 == 1):
                say(f"It will rain tomorrow with {forecast_rain_chances_1} percent chances")
            else:
                say("It will not rain tomorrow")
        elif "snow tomorrow" in text:
            if (forecast_snow_1 == 1):
                say(f"it will snow tomorrow with {forecast_snow_chances_1} percent chances")
            else:
                say("It will not snow tomorrow")
        elif "will it rain" in text:
            if(forecast_rain==1):
                say(f"it will rain today with {forecast_rain_chances} percent chances")
            else:
                say("It will not rain today")
        elif "will it snow" in text:
            if(forecast_snow==1):
                say(f"it will snow today with {forecast_snow_chances} percent chances")
            else:
                say("It will not snow today")
        elif "how is the weather" in text or ("weather today" in text):
            say(f"current weather is {current_text}")
            say(f"temperature is {current_temp} centigrade and")
            say(f" humidity is {current_humidity} percent")
        elif "wind speed" in text:
            say(f"current wind speed is {current_windspeed} kilometers per hour")
        elif "the temperature" in text:
            say(f"current temperature is {current_temp}")
        elif "the humidity" in text:
            say(f"current humidity is {current_humidity}")
        elif ("you" or "your") in text:
            say("I am refrained from answering personal questions.")
        else:
            if flag==0:
                say("I didnt get that")
