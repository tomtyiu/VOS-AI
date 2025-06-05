# VOS-AI

VOS-AI is a voice-operated assistant that lets you control your desktop with speech. It uses OpenAI models for natural language understanding and ElevenLabs for high quality speech synthesis. Whisper is used to transcribe your microphone input. The project includes a simple Tkinter-based GUI and a command line interface.

## Features

- **Voice control for your operating system** – open common Windows applications or perform web searches by speaking.
- **Conversational assistant** – natural conversation powered by OpenAI and Groq models.
- **Run Python snippets** – say "run python" followed by a description and VOS-AI generates and executes the code for you.
- **Text-to-speech output** – responses are spoken using ElevenLabs.
- **Optional GUI** – `vos_ai_gui.py` provides a basic interface with a microphone icon.

## Requirements

- Python 3.8+
- `ffmpeg` installed and available on your `PATH` for audio handling
- Microphone and speakers

Python libraries (install via `pip`): `openai`, `requests`, `whisper`, `torch`, `transformers`, `keyboard`, `pygame`, `elevenlabs`, `groq`, `pyaudio`, `faster-whisper`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/youruser/VOS-AI.git
   cd VOS-AI
   ```

2. Install the dependencies:

   ```bash
   pip install openai requests whisper torch transformers keyboard pygame elevenlabs groq pyaudio faster-whisper
   ```

3. Obtain API keys:

   - `GROQ_API_KEY` – for the Groq language model
   - `ELEVEN_API_KEY` – for ElevenLabs text‑to‑speech
   - `PERPLEXITY_API_KEY` – optional, used by the `AI_search` function

   Export them in your environment or edit `vos_ai.py` to add your keys:

   ```bash
   export GROQ_API_KEY=<your groq key>
   export ELEVEN_API_KEY=<your elevenlabs key>
   export PERPLEXITY_API_KEY=<your perplexity key>
   ```

## Usage

### Command Line

Run the assistant directly in your terminal:

```bash
python vos_ai.py
```

VOS-AI greets you and begins listening. Speak a command when prompted. Press the **spacebar** at any time to exit.

### GUI

A minimal Tkinter GUI is available:

```bash
python vos_ai_gui.py
```

Click the wave icon to start or stop recording. The GUI uses the same logic as the command line tool.

### Running Python code

Say **"run python"** followed by a description of what you want to accomplish. The request is sent to an OpenAI model to generate the code, which is then executed locally. The assistant speaks any output or errors when finished.

## License

This project is released under the [MIT License](LICENSE).

## Disclaimer

VOS-AI is experimental software and may execute commands on your system. Review the generated code before running it and use at your own risk.
