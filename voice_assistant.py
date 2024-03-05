from datetime import datetime
import speech_recognition as sr
from gtts import gTTS
import os
import spacy
import requests
from googlesearch import search
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def process_input(input_text):
    doc = nlp(input_text)

    # Check for specific keywords or entities
    for ent in doc.ents:
        if ent.label_ == "DATE":
            respond_to_date_query(ent.text)
            return

    # Tokenize the input using NLTK
    tokens = word_tokenize(input_text)

    # Perform Part-of-Speech tagging with NLTK
    pos_tags = pos_tag(tokens)

    # Extract nouns and verbs
    nouns = [word for word, pos in pos_tags if pos.startswith('N')]
    verbs = [word for word, pos in pos_tags if pos.startswith('V')]

    if verbs:
        respond_to_something_query()
    else:
        speak("I'm sorry, I didn't understand that.")

def respond_to_date_query(date_text):
    speak(f"Today's date is {date_text}")

def respond_to_something_query():
    speak("I'm here to assist you with something!")

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")

# Rest of the code remains the same...



def google_search(query, num_results=5):
    results = search(query, num_results=num_results, stop=num_results)
    return results

def get_weather(city):
    api_key = "2b0555fd91956770a967a4f1cb6f79b2"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(base_url)
    weather_data = response.json()

    # Example: Print temperature
    temperature = weather_data["main"]["temp"]
    speak(f"The current temperature in {city} is {temperature}°C")

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")

def greet():
    speak("Hello! I'm JASPER. How can I assist you today?")

def get_time():
    current_time = datetime.now().strftime("%H:%M")  # Get current time in HH:MM format
    speak(f"The current time is {current_time}")

def handle_user_input(command):
    process_input(command)  # Add more processing based on Spacy analysis
    
    if "hello" in command:
        greet()
    elif "time" in command:
        get_time()
    elif "weather" in command:
        get_weather("New York")  # You can modify the city as needed
    elif "search" in command:
        query = command.replace("search", "").strip()
        search_results = google_search(query)
        speak("Here are some search results:")
        for result in search_results:
            speak(result)
    elif "exit" in command or "bye" in command:
        speak("Goodbye! Have a great day.")
        return True
    else:
        speak("I'm sorry, I didn't understand that.")

    return False

def main():
    recognizer = sr.Recognizer()

    greet()  # Initial greeting

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You said:", user_input)

            exit_flag = handle_user_input(user_input)
            if exit_flag:
                break

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand your audio.")
        except sr.RequestError as e:
            print(f"Error connecting to the Google API: {e}")

if __name__ == "__main__":
    main()
