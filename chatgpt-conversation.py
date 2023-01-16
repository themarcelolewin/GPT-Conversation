import sounddevice as sd #for accessing my sound devices
import soundfile as sf #requires numpy.  Must install that first.  For reading the audio file.
from gtts import gTTS # Text to Speech conversion
import openai # GPT-3 API
from configparser import ConfigParser #for retrieving environment variables.

#To get speechrecognition to work on a mac, you need to:
#brew install portaudio
#sudo brew link portaudio
#pip install pyaudio
#then install speechrecognition
import speech_recognition as sr

# read in the config file.
config = ConfigParser()
config.read('config.ini')

# Set the API key for OpenAI
openai.api_key = config.get("openai", "api_key")

# use the OpenAI GPT-3 (ChatGPT) model to generate a response to the input text
def generate_response(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).get('choices')[0].get('text')
    return response

#Convert the text from GPT3 to speech
def text_to_speech(text):
    # create a text-to-speech object
    tts = gTTS(text=text)
    
    # saves the tts object to a .wav file.  .mp3's are not supported yet by soundfile library.
    filename = "output.wav"
    tts.save(filename)
    
    # Set the device 
    sd.default.device = 5 #See query below to get your audio output device.
    
    # Play the audio file
    data, sr = sf.read(filename, dtype='int16')
    sd.play(data, sr)
    status = sd.wait()

prev_text = ""

while True:
    # Ask user for a question
    # initialize the recognizer
    r = sr.Recognizer()

    # listen for speech
    with sr.Microphone(device_index=5) as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize the speech
    try:
        text = r.recognize_google(audio, show_all=False)
        print(text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error; {0}".format(e))
        
    prompt = prev_text + text

    # Send it to GPT-3
    chatgpt=generate_response(prompt)
    
    prev_text = chatgpt

    # Print the response form GPT-4
    print(chatgpt)

    # Speak it.
    text_to_speech(chatgpt)

# Needed to find out my sound device numbers.  This will help me do that.
# devices = sd.query_devices()
# for i, device in enumerate(devices):
#     print("Device {}: {}".format(i, device)+"\n")

