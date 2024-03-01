import os
from openai import OpenAI
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
import subprocess
from playsound import playsound

mytext = 'Welcome to me'
language = 'en'
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production
#openai.api_key= os.getenv("OPEN_API_KEY") #'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'
client = OpenAI(api_key="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")

load_dotenv()
model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "Arjun"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?" ]

# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for 'Hello'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hello" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
        
# def get_completion(prompt, model="gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0, # this is the degree of randomness of the model's output
#     )
#     return response.choices[0].message["content"]


def get_completion(prompt, model="gpt-3.5-turbo-0125"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    playsound("listen_chime.mp3")
    while True:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response_text = get_completion(text) #openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{text}"}])
            #response_text = response.choices[0].message.content
            print(response_text)
            # myobj = gTTS(text = response_text, lang = language, slow = False)
            # myobj.save("test.mp3")
            # playsound('test.mp3')
            # speech_file_path = "test.mp3"
            # response = client.audio.speech.create(
            #   model="tts-1",
            #   voice="alloy",
            #   input=response_text
            # )
            
            #response.stream_to_file(speech_file_path)
            # Speak the response
            #print("speaking")
            #playsound(speech_file_path)
            
            #os.system("aplay test.wav")
            
            #os.system("espeak ' "+response_text + "'")
            engine.say(response_text)
            engine.runAndWait()
            playsound("listen_chime.mp3")

            if not audio:
                playsound("error.mp3")
                print("test")
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            playsound("error.mp3")
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
