import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import pyttsx3


def say(text):
    """Speak the text using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


chatStr = ""


def chat(query):
    """Chat with OpenAI's GPT model."""
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\nJarvis: "

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                {"role": "user", "content": query},
            ]
        )
        message = response["choices"][0]["message"]["content"]
        say(message)
        chatStr += f"{message}\n"
        return message
    except openai.error.RateLimitError:
        say("Rate limit exceeded. Please try again later.")
        return "Rate limit exceeded"
    except openai.error.AuthenticationError:
        say("Authentication failed. Please check your API key.")
        return "Authentication error"
    except openai.error.OpenAIError as e:
        say("An error occurred with OpenAI API.")
        print(f"OpenAI Error: {e}")
        return "An error occurred"


def ai(prompt):
    """Generate a response using OpenAI's text generation model."""
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response.choices[0].text.strip()
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)
    except openai.error.OpenAIError as e:
        print(f"Error with OpenAI API: {e}")
        say("Sorry, I couldn't process your request.")


def takeCommand():
    """Take voice input from the user and recognize the speech."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjusts for background noise
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Sorry, I didn't catch that."
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Sorry, I'm having trouble with the speech recognition service."


if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Hello I am Jarvis AI")

    while True:
        print("Listening...")
        query = takeCommand()

        # Open specific sites based on voice input
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]

        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # Open music functionality (macOS specific, modify for other OS if needed)
        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {min} minutes.")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
