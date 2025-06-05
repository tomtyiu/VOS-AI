import tkinter as tk
import threading

import vos_ai


class VoiceGUI:
    def __init__(self, master):
        self.master = master
        master.title("VOS-AI")
        self.recording = False

        self.canvas = tk.Canvas(master, width=64, height=64, highlightthickness=0)
        self._draw_wave()
        self.canvas.bind("<Button-1>", lambda e: self.toggle_record())
        self.canvas.pack(padx=20, pady=20)

    def _draw_wave(self):
        points = []
        for x in range(0, 64, 4):
            y = 32 + int(10 * __import__('math').sin(x / 10.0))
            points.append(x)
            points.append(y)
        self.canvas.create_line(*points, fill="blue", width=2, smooth=True)

    def toggle_record(self):
        if not self.recording:
            self.recording = True
            threading.Thread(target=self.record_loop, daemon=True).start()
        else:
            self.recording = False

    def record_loop(self):
        vos_ai.synthesis("Recording started. Press the icon again to stop.")
        while self.recording:
            vos_ai.recording(vos_ai.WAVE_OUTPUT_FILENAME)
            transcription = vos_ai.transcribe(vos_ai.WAVE_OUTPUT_FILENAME)
            if vos_ai.open_application(transcription):
                pass
            else:
                response = vos_ai.chat(transcription)
                clean = vos_ai.remove_double_stars(response)
                vos_ai.synthesis(clean)
        vos_ai.synthesis("Done. Awaiting your next request.")


def main():
    root = tk.Tk()
    gui = VoiceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
