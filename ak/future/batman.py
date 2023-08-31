import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
# import pyttsx3
from gtts import gTTS
import playsound
import openai

# Initialize OpenAI API with your API key
openai.api_key = "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"

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            conversation_box.insert(tk.END, "You: " + user_input + "\n")
            return user_input
        except sr.UnknownValueError:
            conversation_box.insert(tk.END, "You: [Unrecognized speech]\n")
            return ""

def speak(text):
    tts = gTTS(text)
    tts.save("output.mp3")
    playsound.playsound("output.mp3")

def respond_to_input():
    user_input = input_entry.get()
    conversation_box.insert(tk.END, "You: " + user_input + "\n")
    
    if "exit" in user_input:
        response = "Goodbye, sir."
        conversation_box.insert(tk.END, "BatMan: " + response + "\n")
        speak(response)
        window.after(2000, window.destroy)
    else:
        response = generate_gpt_response(user_input)
        conversation_box.insert(tk.END, "BatMan: " + response + "\n")
        speak(response)

def generate_gpt_response(user_input):
    # Call the GPT-3.5 API to generate a response
    prompt = f"User: {user_input}\nAssistant:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate engine
        prompt=prompt,
        max_tokens=100  # Set the desired length of the response
    )
    return response.choices[0].text.strip()

# Create the main window
window = tk.Tk()
window.title("Batman Voice Assistant")

# Create a scrolled text widget to display the conversation
conversation_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20)
conversation_box.pack()

# Create an entry widget for user input
input_entry = tk.Entry(window, width=40)
input_entry.pack()

# Bind the Enter key to the response function
input_entry.bind("<Return>", respond_to_input)

send_button = tk.Button(window, text="Send", command=respond_to_input)
send_button.pack()

# Create a "Speak" button to listen to user's spoken input
speak_button = tk.Button(window, text="Speak", command=listen)
speak_button.pack()

# Start the GUI event loop
window.mainloop()

