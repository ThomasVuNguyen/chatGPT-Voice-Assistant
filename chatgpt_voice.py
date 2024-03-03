import os
from openai import OpenAI
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
from playsound import playsound

language = 'en'

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()

tts_engine = 'gtts'  # select from 'gtts', 'pyttsx3', 'openai'

engine = pyttsx3.init()
voice = engine.getProperty('voices')[2]
engine.setProperty('voice', voice.id)


def get_completion(messages, model="gpt-3.5-turbo-0125"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1
    )
    return response.choices[0].message.content


load_dotenv()
model = 'gpt-3.5-turbo'


name = "Arjun"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there! How's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             "How can I help?",
             "How's it going my man!"]
#             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?"]

messages = []
# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    # Setup the system message for the GPT
    messages = [{"role": "system",
                 "content": "You are a helpful personal assistant. Try to answer the questions in 100 words or less"}]

    print("Listening for 'Hello'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hello" in text.lower():
                print("Wake word detected.")
                if tts_engine == 'pyttsx3':
                    engine.say(np.random.choice(greetings))
                    engine.runAndWait()
                else:
                    greet = gTTS(text=np.random.choice(greetings), lang=language)
                    greet.save('response.mp3')
                    playsound('response.mp3')

                listen_and_respond(source,messages)
                break
        except sr.UnknownValueError:
            pass
        

# Listen for input and respond with OpenAI API
def listen_and_respond(source, messages):
    playsound("listen_chime.mp3")
    while True:
        print("Listening...")
        audio = r.listen(source, timeout=5)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            messages.append({'role':'user', 'content':text})

            # Send input to OpenAI API
            response_text = get_completion(messages)
            print(response_text)

            if tts_engine == 'pyttsx3':
                engine.say(response_text)
                engine.runAndWait()

            elif tts_engine == 'gtts':
                resp = gTTS(text=response_text, lang=language)
                resp.save('response.mp3')
                playsound('response.mp3')

            elif tts_engine == 'openai':
                response = client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=response_text
                    )

                response.stream_to_file('response.mp3')
                # Speak the response
                print("speaking")
                playsound('response.mp3')

            # Append the response to the response list
            messages.append({'role':'assistant', 'content':response_text})

            playsound("listen_chime.mp3")

            if not audio:
                playsound("error.mp3")
                print("test")
                listen_for_wake_word(source)

        except sr.UnknownValueError:
            playsound("error.mp3")
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
