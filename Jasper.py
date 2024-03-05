# ==== Importing all the necessary libraries
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import nltk
import spacy
from tkinter import *
from PIL import ImageTk
import requests
import pywhatkit  
import pyjokes  

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Download NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# ==== Class JASPER
class JasperAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("JASPER")
        self.root.geometry('600x600')

        self.bg = ImageTk.PhotoImage(file="images/jasper-back.jpg")
        bg = Label(self.root, image=self.bg).place(x=0, y=0, width=600, height=600)

        self.centre = ImageTk.PhotoImage(file="images/flo-motion_5sec.gif")
        left = Label(self.root, image=self.centre).place(x=100, y=100, width=400, height=400)

        # ==== start button
        start = Button(self.root, text='START', font=("times new roman", 14), command=self.start_option).place(x=150, y=520)

        # ==== close button
        close = Button(self.root, text='CLOSE', font=("times new roman", 14), command=self.close_window).place(x=350, y=520)

    # ==== start JASPER
    def start_option(self):
        listener = sr.Recognizer()
        engine = pyttsx3.init()

        # ==== Voice Control
        def speak(text):
            engine.say(text)
            engine.runAndWait()

        # ==== Default Start
        def start():
            # ==== Wish Start
            hour = int(datetime.datetime.now().hour)
            if 0 <= hour < 12:
                wish = "Good Morning!"
            elif 12 <= hour < 18:
                wish = "Good Afternoon!"
            else:
                wish = "Good Evening!"
            speak(f'Hello Sir, {wish} I am JASPER. How may I assist you today?')
            # ==== Wish End

        # ==== Take Command
        def take_command():
            try:
                with sr.Microphone() as data_taker:
                    print("Say Something")
                    voice = listener.listen(data_taker)
                    instruction = listener.recognize_google(voice)
                    instruction = instruction.lower()
                    return instruction
            except:
                pass

        # ==== Run command
        def run_command():
            instruction = take_command()
            print(instruction)
            try:
                if 'who are you' in instruction:
                    speak('I am JASPER, your personal voice Assistant')

                elif 'what can you do for me' in instruction:
                    speak('I can play songs, tell time, provide the current date, check the weather, sing for you, tell jokes, and do simple math')
                
                elif 'what is the meaning of jasper' in instruction:
                    speak("JASPER? Oh, it stands for 'Just A Speech-based Personal Electronic Resource.' But you can also think of me as your magical genie ready to grant your vocal wishes!")


                elif 'current time' in instruction:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    speak('The current time is ' + time)

                elif 'current date' in instruction:
                    date = datetime.datetime.now().strftime('%B %d, %Y')
                    speak('Today is ' + date)

                elif 'weather' in instruction:
                    self.get_weather('Accra', '2b0555fd91956770a967a4f1cb6f79b2')  

                elif 'sing for me' in instruction:
                    speak('Sure, I can sing for you!')
                    pywhatkit.playonyt("Despacito") 

                elif 'tell me a joke' in instruction:
                    joke = pyjokes.get_joke()
                    speak(joke)

                elif 'do some math' in instruction:
                    math_instruction = take_command().lower()

                    # Check for addition
                    if 'plus' in math_instruction:
                        numbers = [int(num) for num in math_instruction.split() if num.isdigit()]
                        if len(numbers) >= 2:
                            result = sum(numbers)
                            speak(f'The result is {result}')
                        else:
                            speak('Sorry, I could not understand the math operation. Please try again.')

                    # Check for subtraction
                    elif 'minus' in math_instruction or 'subtract' in math_instruction:
                        numbers = [int(num) for num in math_instruction.split() if num.isdigit()]
                        if len(numbers) >= 2:
                            result = numbers[0] - numbers[1]
                            speak(f'The result is {result}')
                        else:
                            speak('Sorry, I could not understand the math operation. Please try again.')

                    # Check for multiplication
                    elif 'times' in math_instruction or 'multiply' in math_instruction:
                        numbers = [int(num) for num in math_instruction.split() if num.isdigit()]
                        if len(numbers) >= 2:
                            result = 1
                            for num in numbers:
                                result *= num
                            speak(f'The result is {result}')
                        else:
                            speak('Sorry, I could not understand the math operation. Please try again.')

                    # Check for division
                    elif 'divided by' in math_instruction or 'divide' in math_instruction:
                        numbers = [int(num) for num in math_instruction.split() if num.isdigit()]
                        if len(numbers) >= 2 and numbers[1] != 0:
                            result = numbers[0] / numbers[1]
                            speak(f'The result is {result}')
                        elif numbers[1] == 0:
                            speak("Cannot divide by zero!")
                        else:
                            speak('Sorry, I could not understand the math operation. Please try again.')

                    else:
                        speak('Sorry, I could not understand the math operation. Please try again.')

                elif 'open google' in instruction:
                    speak('Opening Google')
                    webbrowser.open('https://www.google.com')

                elif 'open youtube' in instruction:
                    speak('Opening Youtube')
                    webbrowser.open('https://www.youtube.com')

                elif 'open facebook' in instruction:
                    speak('Opening Facebook')
                    webbrowser.open('https://www.facebook.com')

                elif 'open twitter' in instruction:
                    speak('Opening Twitter')
                    webbrowser.open('https://twitter.com')

                elif 'open linkedin' in instruction:
                    speak('Opening Linkedin')
                    webbrowser.open('https://www.linkedin.com')

                elif 'open gmail' in instruction:
                    speak('Opening Gmail')
                    webbrowser.open('https://www.gmail.com')

                elif 'open canva' in instruction:
                    speak('Opening Canva')
                    webbrowser.open('https://www.canva.com')

                elif 'exit' in instruction:
                    speak('Good bye, let us have another convo next time. It was nice meeting you')
                    self.close_window()
                    return False
                else:
                    speak('I did not understand, can you repeat again')
            except:
                speak('Waiting for your response')
            return True

        # ==== Default Start calling
        start()

        # ==== Run JASPER continuously
        while True:
            if not run_command():
                break

    # ==== Close window
    def close_window(self):
        self.root.destroy()

    def get_weather(self, city, api_key):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        response = requests.get(base_url)
        weather_data = response.json()

        try:
            # Example: Print temperature and description
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            self.speak(f"The current temperature in {city} is {temperature}°C and the weather is {description}.")
        except KeyError:
            self.speak("Sorry, I couldn't retrieve the weather information.")

# ==== create tkinter window
root = Tk()

# === creating object for class
jasper = JasperAssistant(root)

# ==== start the gui
root.mainloop()
