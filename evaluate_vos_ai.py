import json
import os
import time

import vos_ai

# Prompts for conversational evaluation
CHAT_PROMPTS = [
    "Tell me the time.",
    "Who is the president of the United States?"
]

# Commands to test application opening logic
APP_COMMANDS = [
    "open chrome",
    "search google for Python testing"
]

# Optional list of audio files containing spoken commands for evaluation.
AUDIO_FILES = []  # e.g. ["samples/open_chrome.wav"]

def evaluate_chat(prompts):
    results = []
    if vos_ai.OpenAI is None:
        for prompt in prompts:
            results.append({"prompt": prompt, "response": "SKIPPED", "elapsed": 0})
        return results
    for prompt in prompts:
        start = time.time()
        try:
            response = vos_ai.chat(prompt)
        except Exception as e:
            response = f"ERROR: {e}"
        elapsed = time.time() - start
        results.append({"prompt": prompt, "response": response, "elapsed": elapsed})
    return results

def evaluate_open_application(commands):
    results = []
    executed = []

    def dummy_system(cmd):
        executed.append(cmd)

    def dummy_open(url):
        executed.append(url)

    orig_system = vos_ai.os.system
    orig_webopen = vos_ai.webbrowser.open
    vos_ai.os.system = dummy_system
    vos_ai.webbrowser.open = dummy_open

    try:
        for command in commands:
            executed.clear()
            matched = vos_ai.open_application(command)
            results.append({"command": command, "executed": executed[:], "matched": matched})
    finally:
        vos_ai.os.system = orig_system
        vos_ai.webbrowser.open = orig_webopen

    return results


def evaluate_audio_commands(files):
    """Transcribe audio files and run them through open_application."""
    results = []
    if vos_ai.OpenAI is None:
        # Cannot transcribe without OpenAI support
        return results

    for path in files:
        start = time.time()
        try:
            text = vos_ai.transcribe(path)
            executed = []

            def dummy_system(cmd):
                executed.append(cmd)

            def dummy_open(url):
                executed.append(url)

            orig_system = vos_ai.os.system
            orig_open = vos_ai.webbrowser.open
            vos_ai.os.system = dummy_system
            vos_ai.webbrowser.open = dummy_open
            try:
                matched = vos_ai.open_application(text)
            finally:
                vos_ai.os.system = orig_system
                vos_ai.webbrowser.open = orig_open
            elapsed = time.time() - start
            results.append({
                "file": path,
                "transcription": text,
                "executed": executed,
                "matched": matched,
                "elapsed": elapsed,
            })
        except Exception as e:
            results.append({"file": path, "error": str(e)})

    return results


def main():
    chat_results = evaluate_chat(CHAT_PROMPTS)
    app_results = evaluate_open_application(APP_COMMANDS)
    audio_results = evaluate_audio_commands(AUDIO_FILES)

    report = {
        "chat": chat_results,
        "application": app_results,
        "audio": audio_results,
    }
    with open("benchmark_results.json", "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
