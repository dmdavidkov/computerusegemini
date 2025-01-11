# Live API Starter

This project provides a starter kit for building applications that interact with the Gemini API in real-time. It supports audio and video input and provides a set of function tools for interacting with the user's system.

## Installation

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Rename the `.env.example` file to `.env`

3. Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

4. Replace `your_api_key_here` in `.env` with your actual API key.

**Important:** Use headphones when running the script to prevent audio feedback loops.

## Usage

To run the script:

```bash
python main.py
```

The script takes a video-mode flag `--mode`, which can be "camera", "screen", or "none". The default is "screen". To share your screen, run:

```bash
python main.py --mode screen
```

You can also specify the modality to use with the `--modality` flag, which can be "AUDIO" or "TEXT". The default is "AUDIO".

## Function Tools

The `function_tools` directory contains a set of Python scripts that provide various functionalities for interacting with the user's system. These tools can be called by the Gemini model to perform actions such as:

-   `click_mouse.py`: Performs a mouse click at the current cursor position.
-   `copy_and_paste.py`: Inputs text to the screen by simulating typing.
-   `copy_to_clipboard.py`: Copies text to the system clipboard.
-   `execute_js_in_brave.py`: Executes JavaScript code in the currently active chromium based browser window.
-   `function_hub.py`: Manages and executes the available function tools.
-   `get_clipboard.py`: Retrieves the current text from the system clipboard.
-   `move_mouse.py`: Moves the mouse cursor to specified coordinates.
-   `output_text_to_screen.py`: Displays a message on the screen using an alert box.
-   `press_keys.py`: Simulates pressing a single key or a combination of keys.
