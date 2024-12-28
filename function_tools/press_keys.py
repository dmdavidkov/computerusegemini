import asyncio
import time
import pyautogui

VALID_KEYS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    '{', '|', '}', '~',
    'enter', 'esc', 'tab', 'space',
    'ctrl', 'shift', 'alt',
    'win', 'cmd',  # Windows and Command keys
    'up', 'down', 'left', 'right',  # Arrow keys
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'backspace', 'delete', 'insert', 'home', 'end', 'pageup', 'pagedown',
    'capslock', 'numlock', 'scrolllock',
    'printscreen', 'pause',
]

def is_valid_key_combination(keys):
    """Validates if the given key combination is valid."""
    if "+" in keys:
        key_list = keys.split("+")
        for key in key_list:
            if key not in VALID_KEYS:
                return False
    else:
        if keys not in VALID_KEYS:
            return False
    return True

async def press_keys(keys):
    """
    Presses a single key or a combination of keys.

    Args:
        keys: A string representing the key(s) to press. 
              For single keys, it's the key itself (e.g., 'enter', 'a', 'esc').
              For combinations, it's a comma-separated string of keys 
              (e.g., 'ctrl+a', 'shift+tab', 'alt+f4').
    """
    try:
        if not is_valid_key_combination(keys):
            return {"success": False, "error": f"Invalid key combination: {keys}"}

        if "+" in keys:
            # It's a combination
            key_list = keys.split("+")
            pyautogui.hotkey(*key_list)
        else:
            # It's a single key
            pyautogui.press(keys)
        
        time.sleep(0.5) # Introduce a delay

        return {"success": True, "message": f"Pressed key(s): {keys}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_press_keys_tool():
    return {
        "name": "press_keys",
        "description": "Simulates pressing a single key or a combination of keys. Valid keys are: " + ", ".join(VALID_KEYS) + ". For single keys, use the key itself (e.g., 'enter', 'a', 'esc', 'tab'). For combinations, use a '+' separated string (e.g., 'ctrl+a', 'shift+tab', 'alt+f4'). Examples: 'a' (presses the 'a' key), 'enter' (presses the Enter key), 'ctrl+a' (presses Ctrl and A together), 'shift+tab' (presses Shift and Tab together), 'ctrl+shift+s' (presses Ctrl, Shift, and S together).",
        "parameters": {
            "type": "object",
            "properties": {
                "keys": {
                    "type": "string",
                    "description": "The key or combination of keys to press. Must be one of the valid keys. For single keys, provide the key character (e.g., 'a', 'enter', 'esc'). For combinations, use a '+' to separate keys (e.g., 'ctrl+a', 'shift+tab')."
                }
            },
            "required": ["keys"]
        }
    }
