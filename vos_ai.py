# Third-party imports. Some are optional so tests can run without them.
import json
try:
    from openai.types import completion  # type: ignore
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional dependency may be missing
    OpenAI = None
try:
    import requests
except Exception:  # pragma: no cover - optional dependency may be missing
    requests = None
try:
    import whisper
except Exception:  # pragma: no cover - optional dependency may be missing
    whisper = None
try:
    import torch
except Exception:  # pragma: no cover - optional dependency may be missing
    torch = None
#from transformers import pipeline
#from transformers.pipelines.audio_utils import ffmpeg_microphone_live
import sys
try:
    import keyboard
except Exception:  # pragma: no cover - optional dependency may be missing
    keyboard = None
try:
    from pygame import mixer
except Exception:  # pragma: no cover - optional dependency may be missing
    mixer = None
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import stream
    from elevenlabs import play
except Exception:  # pragma: no cover - optional dependency may be missing
    ElevenLabs = None
    stream = None
    play = None
import os
try:
    import pyaudio
except Exception:  # pragma: no cover - optional dependency may be missing
    pyaudio = None
try:
    from faster_whisper import WhisperModel
except Exception:  # pragma: no cover - optional dependency may be missing
    WhisperModel = None
import wave
from urllib.parse import quote
import webbrowser


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
FORMAT = pyaudio.paInt16 if pyaudio else None
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 6
WAVE_OUTPUT_FILENAME = "file.wav"


OUTPUT_PATH = "output.mp3"  # Path to save the output audio file
YOUR_API_KEY = ""

device = "cuda:0" if torch and torch.cuda.is_available() else "cpu"

model = WhisperModel("base") if WhisperModel else None

def transcribe(audio_file):
    """Transcribe audio to text with basic error handling."""
    if OpenAI is None:
        raise ImportError("openai package is required for transcription")
    client = OpenAI()
    try:
        with open(audio_file, "rb") as audio_file_obj:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file_obj
            )
        return transcription.text
    except Exception as e:
        print(f"Transcription failed: {e}")
        return ""


def recording(WAVE_OUTPUT_FILENAME):
    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")
 
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def remove_double_stars(text):
    while text.startswith('**') and text.endswith('**'):
        text = text[2:-2]
    return text

def chat(messages):
    if OpenAI is None:
        raise ImportError("openai package is required for chat functionality")
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "The goal is to have a free-flowing conversation. You can ask questions, provide information, or even tell jokes.. You will respond like a phone conversaiton. You are a voice assistant with emotion and joking tone. End with very response you provide with another question."},
            {"role": "user", "content": messages}
            ]
        )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def search(text):
    if OpenAI is None:
        raise ImportError("openai package is required for web search")
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview"}],
        input=text
    )

    print(response.output_text)
    synthesis(response.output_text)
    

def synthesis(text):
    client = ElevenLabs(
        api_key="", # Defaults to ELEVEN_API_KEY
        )

    audio = client.generate(
        text=text,
        voice="pNInz6obpgDQGcFmaJgB",
        model="eleven_flash_v2_5"
        #stream=True
     )
    play(audio)

def open_application(command):
    """Open an application or perform a Google search based on the command."""
    lower_command = command.lower()
    platform = (
        'win32' if sys.platform.startswith('win') else
        'darwin' if sys.platform.startswith('darwin') else
        'linux'
    )

    applications = {
        'open chrome': {
            'win32': 'start chrome',
            'linux': 'google-chrome',
            'darwin': 'open -a "Google Chrome"'
        },
        'open edge': {
            'win32': 'start msedge',
            'linux': 'microsoft-edge',
            'darwin': 'open -a "Microsoft Edge"'
        },
        'open word': {
            'win32': 'start winword'
        },
        'open spotify': {
            'win32': 'start spotify',
            'darwin': 'open -a Spotify'
        },
        'open outlook': {
            'win32': 'start outlook'
        },
        'open notepad': {
            'win32': 'notepad',
            'linux': 'gedit',
            'darwin': 'open -a TextEdit'
        },
        'open control panel': {'win32': 'control'},
        'open system information window': {'win32': 'msconfig'},
        'open task manager': {'win32': 'taskmgr'},
        'open excel': {'win32': 'start excel'},
        'open user accounts': {'win32': 'netplwiz'},
        'open camera': {
            'win32': 'start microsoft.windows.camera:',
            'darwin': 'open /Applications/Photo\ Booth.app'
        },
        'open file explorer': {
            'win32': 'start explorer',
            'linux': 'xdg-open .',
            'darwin': 'open .'
        },
        'open vs code': {
            'win32': 'start code VoxOS_llama.py',
            'linux': 'code',
            'darwin': 'open -a "Visual Studio Code"'
        },
        'open terminal': {
            'win32': 'start cmd',
            'linux': 'x-terminal-emulator',
            'darwin': 'open -a Terminal'
        },
        'shut down the computer': {'win32': 'shutdown /s /t 30'},
        'exit': {'win32': 'exit()'},
        'end session': {'win32': 'exit()'},
        'open calculator': {
            'win32': 'calc',
            'linux': 'gnome-calculator',
            'darwin': 'open -a Calculator'
        },
        'open paint': {'win32': 'mspaint'},
        'open disk management': {'win32': 'diskmgmt.msc'},
        'open device manager': {'win32': 'devmgmt.msc'},
        'open network connections': {'win32': 'ncpa.cpl'},
        'open power options': {'win32': 'powercfg.cpl'},
        'open remote desktop': {
            'win32': 'mstsc'
        },
        'open settings': {
            'win32': 'start ms-settings:',
            'darwin': 'open -a "System Settings"'
        },
        'restart computer': {'win32': 'shutdown /r /t 10'},
        'lock computer': {'win32': 'rundll32.exe user32.dll,LockWorkStation'},
    }

    for app_command, platform_cmds in applications.items():
        if app_command in lower_command:
            system_command = platform_cmds.get(platform)
            if system_command:
                synthesis("Openning applicaiton now")
                os.system(system_command)
                return True
            else:
                print(f"Platform '{platform}' not supported for command '{app_command}'")
                return False
    if 'search google for' in lower_command:
        # Extracting the query after the specific phrase
        query = lower_command.split('search google for')[-1].strip()
        # Properly escaping the query for use in a URL
        safe_query = quote(query)
        # Open the default web browser with the Google search URL
        webbrowser.open(f"https://www.google.com/search?q={safe_query}")
        return True
    if 'direction to' in command.lower():
        query = command.lower().split('direction to')[-1].strip()
        if query:  # Check if the query is not empty
            url = f"https://www.google.com/maps/place/{query}"
            webbrowser.open(url)
            return True
    if 'play pandora' in command.lower():
        #query = command.split('search google for')[-1].strip()
        os.system(f"start msedge https://www.pandora.com/station")
        return True
    if 'open youtube' in command.lower():
        #query = command.split('search google for')[-1].strip()
        os.system(f"start msedge https://www.youtube.com/")
        return True
    if 'open wikipedia' in command.lower():
        #query = command.split('search google for')[-1].strip()
        os.system(f"start msedge https://www.wikipedia.org/")
        return True
    if 'open ChatGPT' in command.lower():
        #query = command.split('search google for')[-1].strip()
        os.system(f"start msedge https://chat.openai.com/")
        return True
    if 'search mode' in command.lower():
        synthesis('What are you searching for?')
        recording(WAVE_OUTPUT_FILENAME)  # Record voice input
        transcription = transcribe(WAVE_OUTPUT_FILENAME)  # Transcribe the audio file
        print(transcription)
        search(transcription)
        return True
    return False  # Indicates no application command was executed

def AI_search(text):
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise. summarize the content"
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }
    #Headers with API key included
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {YOUR_API_KEY}"  # Authorization header with the API key
        }

    # Making the HTTP POST request
    response = requests.post(url, json=payload, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the JSON response
        response_data = response.json()
        # Navigating to the nested 'message' content inside 'choices'
        try:
            message_content = response_data['choices'][0]['message']['content']
            #message_content=response.text
            print("Message, content:", message_content)
            clean_text = remove_double_stars(message_content)  # Clean the response text
            synthesis(message_content)  # Convert text to speech

        except KeyError as e:
            print(f"Key error: {str(e)} - Check the JSON structure.")
        except IndexError as e:
            print(f"Index error: {str(e)} - Check the list indices.")
    else:
        print("Failed to fetch data:", response.status_code)

def main():
    print("Running VoxOS. Press spacebar to stop.")
    synthesis("This is Vox O.S.  Your O.S voice assistant. How can I help you today?")  # Convert text to speech
    while not keyboard.is_pressed('space'):
        print("Enter Voice Prompt")
        recording(WAVE_OUTPUT_FILENAME)  # Record voice input
        transcription = transcribe(WAVE_OUTPUT_FILENAME)  # Transcribe the audio file
        print("Vox:", transcription)            
        if open_application(transcription):  # Check if it's an application command
            print("Application command processed.")
        else:
            # Handle as normal user input
            #messages = [{"role": "system", "content": "You are an personal assistant that perform multiple tasks, check weather, stocks, news, latest songs, latest products, facts, science, biology, chemistry, science, politics, marketing, business and others. Your name is Bob. You respond with concise and short responses. You are confident and professional. You are having a vocal conversation with a user. You will never output any markdown or formatted text of any kind, and you will speak in a concise, shighly conversational manner. You troubleshoot and don't hesitate to send it to repair to repair facility after troubleshooting. You will adopt any persona that the user may ask of you."}]
            #You will adopt any persona that the user may ask of you. You provide latest weather report, latest sport news, finances, poetry, latest news reports, science and technology news.
            user_input = transcription  # Process user's spoken input
            if not user_input:
                print("No input detected. Please try again.")
                continue  # Skip if transcription is empty
            
            #messages.append({"role": "user", "content": user_input})
            response = chat(user_input)  # Get chat model response
            clean_text = remove_double_stars(response)  # Clean the response text
            synthesis(clean_text)  # Convert text to speech
            #messages.append({"role": "assistant", "content": response})  # Log the assistant's response
            print("Response processed and spoken.")
        print("\n\n")

if __name__ == "__main__":
    main()
