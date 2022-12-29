import speech_recognition as sr
from gtts import gTTS
import playsound
import openai
from configparser import ConfigParser

configur = ConfigParser()
configur.read('config.ini')

openai.api_key = configur.get("openai", "api_key")

def generate_response(text):
    # use the OpenAI GPT-3 (ChatGPT) model to generate a response to the input text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).get('choices')[0].get('text')

    # return the generated response
    return response

# initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()

# create a function to recognize and repeat the voice input
def recognize_and_repeat():
    # get the audio input from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)        

    # try to recognize the speech using Google's speech recognition API
    try:
        print("Processing")
        text = r.recognize_google(audio)
        print(text)
        
        chatgpt=generate_response(text)
        
        tts = gTTS(text=chatgpt)
        print(chatgpt)
        tts.save("output.mp3")
        playsound.playsound("output.mp3")


    except sr.UnknownValueError:
        # if speech is not recognized, print an error message
        print("Sorry, I could not understand what you said")
        
    if text.lower() == "goodbye":
        return False
    else:
        return True

# run the recognize_and_repeat function when the script is executed
if __name__ == "__main__":
    keep_going = True
    while keep_going:
        keep_going = recognize_and_repeat()