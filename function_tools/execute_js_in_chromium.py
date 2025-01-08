import asyncio
import pyautogui
import pyperclip

async def execute_js_in_chromium(js_code: str):
    """
    Executes the given JavaScript code in the currently active Chromium browser window.

    Opens Chromium's developer tools, navigates to the console, pastes the code, and executes it.
    """
    try:
        # Simulate pressing Ctrl+Shift+J (or Cmd+Option+J on macOS) to open the console
        pyautogui.hotkey('ctrl', 'shift', 'j')
        await asyncio.sleep(0.5)  # Wait for the console to open

        # Copy the JavaScript code to the clipboard
        pyperclip.copy(js_code)

        # Simulate pressing Ctrl+V (or Cmd+V on macOS) to paste the code
        pyautogui.hotkey('ctrl', 'v')
        await asyncio.sleep(0.5)  # Wait for the code to be pasted

        # Simulate pressing Enter to execute the code
        pyautogui.press('enter')
        await asyncio.sleep(1)  # Wait for the console to open

        # Simulate pressing Ctrl+Shift+J (or Cmd+Option+J on macOS) to open the console
        pyautogui.hotkey('ctrl', 'shift', 'j')

        return {"success": True, "message": f"Executed JavaScript code in browser: {js_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_execute_js_in_chromium_tool():
    """
    Returns the tool definition for the execute_js_in_chromium function.
    """
    return {
        "name": "execute_js_in_chromium",
        "description": "Executes JavaScript code in the currently active Chromium based browser window. Useful for automating interactions with web pages or accessing browser-specific functionality.",
        "parameters": {
            "type": "object",
            "properties": {
                "js_code": {
                    "type": "string",
                    "description": "The JavaScript code to execute."
                }
            },
            "required": ["js_code"]
        }
    }
