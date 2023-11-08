# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings
import speech_recognition as sr
import openai
import wikipedia
import os
import webbrowser
import datetime

api_key = "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"
openai.api_key = api_key


def say(text):
    os.system(f"say {text}")


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("raj")
    say("Hello I am Krim")
    while True:
        print("Listening...")
        text = takeCommand().lower()
        sites = [["youtube", "https://www.youtube.com/"], ["firefox", "https://www.firefox.com/"],
                 ["google", "https://www.google.com/"], ["wikipedia", "https://www.wikipedia.com/"]]
        for site in sites:
            if f"open {site[0]}" in text:
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
        apps = [["music", "/System/Applications/Music.app"],
                ["powerpoint", "/Applications/\"Microsoft PowerPoint.app\""],
                ["vs code", "/Applications/\"Visual Studio Code.app\""]]
        for app in apps:
            if f"open {app[0]}" in text:
                say(f"Opening {app[0]}")
                os.system(f"open {app[1]}")
        if "the time" in text:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strfTime}")
        if "using ai" in text:
            prompt = text
            response = openai.Completion.create(
                engine="text-davinci-002",  # Choose the engine that fits your needs
                prompt=prompt,
                max_tokens=50  # Adjust the response length as needed
            )
            translated_text = response.choices[0].text
            say(translated_text)
        if ("search" or "what" or "who") in text:
                text = text.replace("search", "")
                text = text.replace("what", "")
                text = text.replace("who", "")
                text = text.replace("is", "")
                text = text.replace("are", "")
                ans = wikipedia.summary(text, sentences=1)
                print(ans)
                say("according to wikipedia")
                say(ans)
        if ("you" or "your") in text:
            say("I don't have my personal opinions.")
        if "sent email" in text:
            try:
                say("what should I say")

        if "close" in text:
            say("bye")
            break

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
