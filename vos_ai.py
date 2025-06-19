import json
import sys
import os
import wave
from urllib.parse import quote
import webbrowser

# Optional heavy dependencies are imported lazily so the module can be used for
# testing without them installed.
try:  # type: ignore
    from openai import OpenAI  # noqa: F401
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

try:  # type: ignore
    import requests  # noqa: F401
except Exception:  # pragma: no cover
    requests = None  # type: ignore

try:  # type: ignore
    import whisper  # noqa: F401
except Exception:  # pragma: no cover
    whisper = None  # type: ignore

try:  # type: ignore
    import torch
except Exception:  # pragma: no cover
    torch = None  # type: ignore

try:  # type: ignore
    import keyboard  # noqa: F401
except Exception:  # pragma: no cover
    keyboard = None  # type: no cover

try:  # type: ignore
    from pygame import mixer  # noqa: F401
except Exception:  # pragma: no cover
    mixer = None  # type: ignore

try:  # type: ignore
    from elevenlabs.client import ElevenLabs  # noqa: F401
    from elevenlabs import play  # noqa: F401
except Exception:  # pragma: no cover
    ElevenLabs = None  # type: ignore
    def play(audio):  # type: ignore
        pass

try:  # type: ignore
    import pyaudio
except Exception:  # pragma: no cover
    pyaudio = None  # type: ignore

try:  # type: ignore
    from faster_whisper import WhisperModel  # noqa: F401
except Exception:  # pragma: no cover
    WhisperModel = None  # type: ignore


os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
if pyaudio:
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 6
else:  # pragma: no cover - missing audio support
    FORMAT = CHANNELS = RATE = CHUNK = RECORD_SECONDS = None
WAVE_OUTPUT_FILENAME = "file.wav"


OUTPUT_PATH = "output.mp3"  # Path to save the output audio file
YOUR_API_KEY = ""

if torch and hasattr(torch, "cuda") and torch.cuda.is_available():
    device = "cuda:0"
else:
    device = "cpu"

model = WhisperModel("base") if WhisperModel else None

def transcribe(audio_file):
    """Transcribe audio to text using OpenAI if available."""
    if OpenAI is None:  # pragma: no cover - optional dependency missing
        raise RuntimeError("OpenAI package not installed")

    client = OpenAI()
    audio_file = open(audio_file, "rb")

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file,
    )

    return transcription.text


def recording(WAVE_OUTPUT_FILENAME):
    if pyaudio is None:  # pragma: no cover - optional dependency missing
        raise RuntimeError("pyaudio package not installed")

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
    from openai import OpenAI
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
    from openai import OpenAI
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview"}],
        input=text
    )

    print(response.output_text)
    synthesis(response.output_text)
    

def synthesis(text):
    """Convert text to speech if ElevenLabs is available."""
    if ElevenLabs is None:  # pragma: no cover
        print(text)
        return

    client = ElevenLabs(api_key=os.environ.get("ELEVEN_API_KEY", ""))

    audio = client.generate(
        text=text,
        voice="pNInz6obpgDQGcFmaJgB",
        model="eleven_flash_v2_5",
    )
    play(audio)

def open_application(command):
    """Open an application or perform a Google search based on the command."""
    lower_command = command.lower()
    applications = {
        'open chrome': "start chrome",
        'open edge': "start msedge",
        'open word': "start winword",
        'open spotify': "start spotify",
        'open outlook': "start outlook",
        'open notepad': "notepad",
        'open control panel': "control",
        'open system information window': "msconfig",
        'open task manager': "taskmgr",
        'open excel': "start excel",
        'open user accounts': "netplwiz",
        'open camera': "start microsoft.windows.camera:",
        'open file explorer': "start explorer",
        'open vs Code': "start code VoxOS_llama.py",
        'shut down the computer': "shutdown /s /t 30",
        'exit': "exit()",
        'end session': "exit()",
        # New entries
        'open calculator': "calc",
        'open paint': "mspaint",
        'open disk management': "diskmgmt.msc",
        'open device manager': "devmgmt.msc",
        'open network connections': "ncpa.cpl",
        'open power options': "powercfg.cpl",
        'open remote desktop': "mstsc",
        'open settings': "start ms-settings:",
        'restart computer': "shutdown /r /t 10",
        'lock computer': "rundll32.exe user32.dll,LockWorkStation",
        }

    for app_command, system_command in applications.items():
        if app_command in command.lower():
            synthesis("Openning applicaiton now")
            os.system(system_command)
            return True  # Indicates that an application command was executed
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
    if requests is None:  # pragma: no cover - optional dependency missing
        raise RuntimeError("requests package not installed")

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
