import asyncio
import pyperclip

async def get_clipboard():
    """Get the current text from the system clipboard"""
    try:
        text = await asyncio.to_thread(pyperclip.paste)
        return {"success": True, "message": "Successfully retrieved clipboard text.", "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_get_clipboard_tool():
    return {
        "name": "get_clipboard",
        "description": "Get the current text from the system clipboard.",
    }
