# VOS-AI
Voice operating system controls using Voice

## GUI

Run `vos_ai_gui.py` for a simple interface with a wave icon. Click the icon to start or stop recording. Spoken commands are processed using the existing `vos_ai.py` logic.

## Running Python Commands

Say "run python" followed by a description of what you want. The request is sent to OpenAI to generate Python code, which is then executed locally. The assistant reads any output or errors aloud and lets you know when it's finished.
