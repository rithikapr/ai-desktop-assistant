import os
import platform
import subprocess
import warnings
from datetime import datetime
from PIL import ImageGrab
import psutil
import screen_brightness_control as sbc  # type: ignore
from langchain_community.llms import Ollama  # type: ignore
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore
from comtypes import CLSCTX_ALL  # type: ignore
import ctypes
import tkinter as tk
from tkinter import scrolledtext

warnings.filterwarnings("ignore")


class AIDesktopAssistant:
    def __init__(self):
        self.llm = Ollama(model="phi3", temperature=0.3, num_thread=4)

    def _adjust_brightness(self, level: str) -> str:
        try:
            level = max(0, min(100, int(level)))
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except Exception as e:
            return f"Error setting brightness: {str(e)}"

    def _increase_brightness(self, amount: str = "10") -> str:
        try:
            current = sbc.get_brightness(display=0)[0]
            level = max(0, min(100, current + int(amount)))
            sbc.set_brightness(level)
            return f"Brightness increased to {level}%"
        except Exception as e:
            return f"Error increasing brightness: {str(e)}"

    def _decrease_brightness(self, amount: str = "10") -> str:
        try:
            current = sbc.get_brightness(display=0)[0]
            level = max(0, min(100, current - int(amount)))
            sbc.set_brightness(level)
            return f"Brightness decreased to {level}%"
        except Exception as e:
            return f"Error decreasing brightness: {str(e)}"

    def _take_screenshot(self) -> str:
        try:
            desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            path = os.path.join(desktop, filename)
            ImageGrab.grab().save(path)
            return f"Screenshot saved as '{filename}' on Desktop"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    def _show_battery(self) -> str:
        try:
            battery = psutil.sensors_battery()
            percent = battery.percent
            charging = battery.power_plugged
            status = "Charging" if charging else "Not charging"
            return f"Battery is at {percent}% ({status})"
        except Exception as e:
            return f"Error getting battery status: {str(e)}"

    def _get_volume(self) -> str:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            level = volume.GetMasterVolumeLevelScalar()
            return f"Current volume is at {int(level * 100)}%"
        except Exception as e:
            return f"Error retrieving volume: {str(e)}"

    def _increase_volume(self, amount: str = "10") -> str:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            new_level = min(1.0, current + int(amount) / 100)
            volume.SetMasterVolumeLevelScalar(new_level, None)
            return f"Volume increased to {int(new_level * 100)}%"
        except Exception as e:
            return f"Error increasing volume: {str(e)}"

    def _decrease_volume(self, amount: str = "10") -> str:
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            new_level = max(0.0, current - int(amount) / 100)
            volume.SetMasterVolumeLevelScalar(new_level, None)
            return f"Volume decreased to {int(new_level * 100)}%"
        except Exception as e:
            return f"Error decreasing volume: {str(e)}"

    def _get_datetime(self) -> str:
        now = datetime.now()
        return now.strftime("Today is %A, %B %d, %Y and the time is %I:%M %p")

    def _open_app(self, app_name: str) -> str:
        app_map = {
            "calculator": "C:/Windows/System32/calc.exe",
            "notepad": "C:/Program Files/Notepad++/notepad++.exe"
                            }
        try:
            app_name = app_name.strip().lower()
            if app_name in app_map:
                subprocess.Popen([app_map[app_name]])
                return f"Opening {app_name}"
            else:
                return f"Unknown app: {app_name}. Try again."
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"

    def _determine_action(self, user_input: str) -> str:
        user_input = user_input.lower().strip()
        # Manual fallback for better accuracy
        if any(kw in user_input for kw in ["what time", "what day", "current time", "date"]):
            return "show_datetime"

        prompt = f"""
You are a smart assistant. Based on the user's command, return one of the following exact formats (no extra text):

- adjust_brightness <number>
- increase_brightness <number>
- decrease_brightness <number>
- take_screenshot
- show_battery
- show_volume
- increase_volume <number>
- decrease_volume <number>
- show_datetime
- open_app <appname>

Examples:
"Set brightness to 70" → adjust_brightness 70
"Increase brightness by 20" → increase_brightness 20
"Decrease brightness" → decrease_brightness 10
"Take a screenshot" → take_screenshot
"Battery level" → show_battery
"What is the battery status?" → show_battery
"What's the volume?" → show_volume
"Increase volume by 10" → increase_volume 10
"What day is today?" → show_datetime
"Open calculator" → open_app calculator

User said: "{user_input}"
Reply with just the correct command:
"""
        return self.llm.invoke(prompt).strip().lower()

class ChatGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title("AI Desktop Assistant")
        self.root.state("zoomed")
        self.root.configure(bg="#f0f4f7")

        self.chat_display = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Segoe UI", 12),
            bg="white",
            fg="black",
            relief="flat",
        )
        self.chat_display.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        self.entry_frame = tk.Frame(self.root, bg="#f0f4f7")
        self.entry_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.entry = tk.Entry(
            self.entry_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="black",
            relief="solid",
            bd=1,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.entry_frame,
            text="Send",
            font=("Segoe UI", 11, "bold"),
            bg="#007acc",
            fg="white",
            command=self.send_message,
            padx=20,
            pady=5,
        )
        self.send_button.pack(side=tk.RIGHT)

        self._add_chat(
            "Assistant",
            "Hi! I'm your desktop assistant. Try:\n• Increase brightness\n• Take a screenshot\n• Open notepad\n• What time is it?",
            "#003399",
        )

    def _add_chat(self, speaker, message, color):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%I:%M %p")
        self.chat_display.insert(
            tk.END, f"{speaker} [{timestamp}]:\n", ("speaker",)
        )
        self.chat_display.insert(tk.END, f"{message}\n\n", ("message",))
        self.chat_display.tag_config("speaker", foreground=color, font=("Segoe UI", 12, "bold"))
        self.chat_display.tag_config("message", font=("Segoe UI", 12))
        self.chat_display.yview(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def send_message(self, event=None):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)
        self._add_chat("You", user_input, "#000000")

        try:
            command = self.assistant._determine_action(user_input)

            if command.startswith("adjust_brightness"):
                response = self.assistant._adjust_brightness(command.split()[-1])
            elif command.startswith("increase_brightness"):
                parts = command.split()
                amount = parts[1] if len(parts) > 1 else "10"
                response = self.assistant._increase_brightness(amount)
            elif command.startswith("decrease_brightness"):
                parts = command.split()
                amount = parts[1] if len(parts) > 1 else "10"
                response = self.assistant._decrease_brightness(amount)
            elif command == "take_screenshot":
                response = self.assistant._take_screenshot()
            elif command == "show_battery":
                response = self.assistant._show_battery()
            elif command == "show_volume":
                response = self.assistant._get_volume()
            elif command.startswith("increase_volume"):
                parts = command.split()
                amount = parts[1] if len(parts) > 1 else "10"
                response = self.assistant._increase_volume(amount)
            elif command.startswith("decrease_volume"):
                parts = command.split()
                amount = parts[1] if len(parts) > 1 else "10"
                response = self.assistant._decrease_volume(amount)
            elif command == "show_datetime":
                response = self.assistant._get_datetime()
            elif command.startswith("open_app"):
                response = self.assistant._open_app(command.split(" ", 1)[1])
            else:
                response = "Sorry, I didn’t understand that."

        except Exception as e:
            response = f"Error: {str(e)}"

        self._add_chat("Assistant", response, "#003399")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    if platform.system() != "Windows":
        print("This assistant currently supports only Windows.")
    else:
        assistant = AIDesktopAssistant()
        ChatGUI(assistant).run()
