import json
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

def evaluate_chat(prompts):
    results = []
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


def main():
    chat_results = evaluate_chat(CHAT_PROMPTS)
    app_results = evaluate_open_application(APP_COMMANDS)
    report = {"chat": chat_results, "application": app_results}
    with open("benchmark_results.json", "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
