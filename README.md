# AI Desktop Assistant (GUI & CLI Version)

## Overview
An **offline AI-powered desktop assistant** that uses a local LLM (**phi3 via Ollama**) to understand natural language commands and perform system-level tasks such as:

- 🔆 Adjusting screen brightness
- 🔊 Controlling system volume
- 🖼️ Taking screenshots
- 🔋 Checking battery status
- 🕒 Showing date/time
- 🗂️ Opening applications (e.g., Notepad, Calculator)

Supports both **GUI (Tkinter)** and **CLI** modes.

- **LLM Model:** [phi3](https://ollama.com/library/phi3)
- **LLM Runtime:** [Ollama](https://ollama.com/)
- **LangChain Integration:** For structured command interpretation
- **Offline:**  Fully local, no internet needed

---

##  Setup Instructions

### 1. Clone the Repository (optional)
bash
git clone https://github.com/rithikapr/ai-desktop-assistant.git
cd ai-desktop-assistant


### 2. Create & Activate Virtual Environment (optional)
bash
python -m venv venv
venv\Scripts\activate  # Windows only

### 3. Install Python Dependencies
bash
pip install -r requirements.txt

### 4. (Optional) Manual Dependency Install
If `requirements.txt` is missing:
bash
pip install langchain langchain-community pillow screen-brightness-control pydantic SQLAlchemy psutil pycaw
ttkbootstrap 

### 5. Install & Run Ollama
- Download Ollama: [https://ollama.com/download](https://ollama.com/download)
- In terminal:
bash
ollama pull phi3
ollama run phi3

 **Note:** Ollama must be running in the background for the assistant to work.

##  How to Run

### CLI Version
bash
python cli_main.py


### 🖼️ GUI Version
bash
python gui_main.py


---

##  Supported Commands (Examples)

|  User Query                         |  Interpreted As              |
|-------------------------------------|--------------------------------|
| Set brightness to 70                | `adjust_brightness 70`         |
| Increase brightness by 20           | `increase_brightness 20`       |
| Decrease the brightness             | `decrease_brightness 10`       |
| What is the battery status?         | `show_battery`                 |
| Take a screenshot                   | `take_screenshot`              |
| What time is it?                    | `show_datetime`                |
| What’s the volume?                  | `show_volume`                  |
| Increase volume by 10               | `increase_volume 10`           |
| Decrease volume                     | `decrease_volume 10`           |
| Open calculator                     | `open_app calculator`          |
| Launch notepad                      | `open_app notepad`             |

---

##  File Structure

.
├── cli_main.py         # CLI assistant logic
├── gui_main.py         # GUI assistant logic using Tkinter
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── venv/               # Virtual environment folder

##  Notes

-  Supports only **Windows OS**
-  App paths (like Notepad++ or calculator) may need to be updated inside `open_app()` function
-  Default volume/brightness adjustment is **±10%** if no value is given
-  Works best with `phi3` via Ollama
