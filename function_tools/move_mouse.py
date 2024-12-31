import asyncio
import pyautogui

async def move_mouse(x: int, y: int):
    """Moves the mouse to the specified coordinates, scaling from a 1920x1080 resolution."""
    try:
        screen_width, screen_height = pyautogui.size()
        scaled_x = int(x * (screen_width / 1920))
        scaled_y = int(y * (screen_height / 1080))
        pyautogui.moveTo(scaled_x, scaled_y)
        return {"success": True, "message": f"Moved mouse to ({x}, {y}). Look at the last screen capture to see the mouse cursor at the new position. Adjust with a new function call if needed."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_move_mouse_tool():
    return {
        "name": "move_mouse",
        "description": "Moves the mouse cursor to the specified coordinates.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "The x-coordinate to move the mouse to."
                },
                "y": {
                    "type": "integer",
                    "description": "The y-coordinate to move the mouse to."
                }
            },
            "required": ["x", "y"]
        }
    }
