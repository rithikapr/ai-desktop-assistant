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

warnings.filterwarnings("ignore")

class AIDesktopAssistantCLI:
    def __init__(self):
        self.llm = Ollama(model="phi3", temperature=0.3, num_thread=4)

    def _adjust_brightness(self, level: str) -> str:
        try:
            level = max(0, min(100, int(level)))
            sbc.set_brightness(level)
            return f"Brightness set to {level}%"
        except Exception as e:
            return f"Error setting brightness: {str(e)}"

    def _increase_brightness(self, amount: str) -> str:
        try:
            current = sbc.get_brightness(display=0)[0]
            level = max(0, min(100, current + int(amount)))
            sbc.set_brightness(level)
            return f"Brightness increased to {level}%"
        except Exception as e:
            return f"Error increasing brightness: {str(e)}"

    def _decrease_brightness(self, amount: str) -> str:
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

    def _increase_volume(self, amount: str) -> str:
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

    def _decrease_volume(self, amount: str) -> str:
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
                return f"Unknown app: {app_name}. Try calculator, notepad, etc."
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"

    def _determine_action(self, user_input: str) -> str:
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
"Increase the brightness" → increase_brightness 10
"Decrease the brightness by 30" → decrease_brightness 30
"Decrease the brightness" → decrease_brightness 10
"Take a screenshot" → take_screenshot
"Battery level" → show_battery
"What is the battery status?" → show_battery
"What's the volume?" → show_volume
"Increase volume by 10" → increase_volume 10
"Decrease volume by 10" → decrease_volume 10
"What time is it?" → show_datetime
"Open calculator" → open_app calculator
"Launch notepad" → open_app notepad

User said: "{user_input}"
Reply with just the correct command:
"""
        return self.llm.invoke(prompt).strip().lower()

    def run(self):
        print("\n🤖 Welcome to the AI Desktop Assistant (CLI Version)")
        print("Type 'exit' to quit. Try commands like: 'Increase brightness by 20', 'Take a screenshot', 'Open notepad'...\n")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Assistant: Goodbye!")
                break

            try:
                command = self._determine_action(user_input)

                if command.startswith("adjust_brightness"):
                    response = self._adjust_brightness(command.split()[-1])
                elif command.startswith("increase_brightness"):
                    parts = command.split()
                    amount = parts[1] if len(parts) > 1 else "10"
                    response = self._increase_brightness(amount)
                elif command.startswith("decrease_brightness"):
                    parts = command.split()
                    amount = parts[1] if len(parts) > 1 else "10"
                    response = self._decrease_brightness(amount)
                elif command == "take_screenshot":
                    response = self._take_screenshot()
                elif command == "show_battery":
                    response = self._show_battery()
                elif command == "show_volume":
                    response = self._get_volume()
                elif command.startswith("increase_volume"):
                    parts = command.split()
                    amount = parts[1] if len(parts) > 1 else "10"
                    response = self._increase_volume(amount)
                elif command.startswith("decrease_volume"):
                    parts = command.split()
                    amount = parts[1] if len(parts) > 1 else "10"
                    response = self._decrease_volume(amount)
                elif command == "show_datetime":
                    response = self._get_datetime()
                elif command.startswith("open_app"):
                    response = self._open_app(command.split(" ", 1)[1])
                else:
                    response = "Sorry, I didn’t understand that."

            except Exception as e:
                response = f"Error: {str(e)}"

            print("Assistant:", response)


if __name__ == "__main__":
    if platform.system() != "Windows":
        print("This assistant currently supports only Windows.")
    else:
        assistant = AIDesktopAssistantCLI()
        assistant.run()