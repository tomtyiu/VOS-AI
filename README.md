# VOS-AI

VOS-AI is a voice-operated assistant that uses speech recognition and AI models to control your desktop. It relies on OpenAI and Groq for natural language understanding and ElevenLabs for text-to-speech.

## Features

- **Voice commands** for common desktop actions and web searches
- **Conversational assistant** powered by OpenAI and Groq models
- **Run Python snippets** by saying "run python" and describing the code
- **Speech synthesis** using ElevenLabs
- Works from the command line (a GUI is planned)

## Requirements

- Python 3.8 or newer
- `ffmpeg` available on your `PATH`
- Microphone and speakers
- Python libraries: `openai`, `requests`, `whisper`, `torch`, `transformers`, `keyboard`, `pygame`, `elevenlabs`, `groq`, `pyaudio`, `faster-whisper`

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/youruser/VOS-AI.git
   cd VOS-AI
   ```
2. Install dependencies
   ```bash
   pip install openai requests whisper torch transformers keyboard pygame elevenlabs groq pyaudio faster-whisper
   ```
3. Export your API keys (replace with your own)
   ```bash
   export GROQ_API_KEY=<your groq key>
   export ELEVEN_API_KEY=<your elevenlabs key>
   export PERPLEXITY_API_KEY=<your perplexity key>  # optional
   ```

## Usage

Run the assistant in your terminal:
```bash
python vos_ai.py
```
Speak a command when prompted. Press the **spacebar** at any time to exit.

Say **"run python"** followed by a description of the code you want to generate and execute.

## TODO

- Cross-platform support for Linux and macOS
- User-friendly GUI interface
- More built-in voice commands
- Better error handling for speech recognition
## Finished:
- Removed hard-coded API keys from the source

## License

This project is released under the [MIT License](LICENSE).

## Disclaimer

VOS-AI is experimental software and may execute commands on your system. Review the generated code before running it and use at your own risk.
