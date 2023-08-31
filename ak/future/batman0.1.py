import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from gtts import gTTS
import playsound
import webbrowser
import datetime

recognizer = sr.Recognizer()

commands = {
    "hello": "Hello, sir! How can I assist you today?",
    "open browser": "Opening web browser.",
    "search": "Sure, what would you like to search for?",
    "time": "The current time is {}.",
    "exit": "Goodbye, sir."
}

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print("You:", user_input)
            return user_input
        except sr.UnknownValueError:
            print("Sorry, could not understand your audio.")
            return ""
        

def speak(text):
    tts = gTTS(text)
    tts.save("output.mp3")
    playsound.playsound("output.mp3")
    

def respond_to_input(command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        response = commands["time"].format(current_time)
    elif "search" in command:
        response = commands["search"]
        user_input = listen()
        webbrowser.open_new_tab(f"https://www.google.com/search?q={user_input}")
    else:
        response = commands.get(command.lower(), "I'm not sure how to respond to that, sir.")
    conversation_box.insert(tk.END, "You: " + command + "\n")
    conversation_box.insert(tk.END, "BatMan: " + response + "\n")
    speak(response)

# Create the main window
window = tk.Tk()
window.title("BatMan Voice Assistant")

# Create a scrolled text widget to display the conversation
conversation_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20)
conversation_box.pack()

# Create a "Speak" button to listen to user's spoken input
def speak_button_callback():
    user_input = listen()
    respond_to_input(user_input)

speak_button = tk.Button(window, text="Speak", command=speak_button_callback)
speak_button.pack()

# Start the GUI event loop
window.mainloop()
