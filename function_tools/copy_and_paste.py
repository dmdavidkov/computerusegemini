import asyncio
import pyautogui
import pyperclip

async def input_text_to_screen(text):
    """Input text to the screen (simulating typing)"""
    try:
        # Simulate typing the text
        pyautogui.typewrite(text)

        return {"success": True, "message": f"Inputted text: {text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_input_text_to_screen_tool():
    return {
        "name": "input_text_to_screen",
        "description": "Triggers input on the screen in the current cursor position. Useful for automating text input into forms, text editors, or any active field.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text content to be typed into the active application."
                }
            },
            "required": ["text"]
        }
    }
