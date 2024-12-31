import asyncio
import pyautogui

async def click_mouse():
    """Performs a mouse click at the current cursor position."""
    try:
        pyautogui.click()
        return {"success": True, "message": "Clicked mouse at current position."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_click_mouse_tool():
    return {
        "name": "click_mouse",
        "description": "Performs a mouse click at the curren cursor position.",
    }

