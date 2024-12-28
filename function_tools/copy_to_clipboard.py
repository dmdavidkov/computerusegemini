import asyncio
import pyperclip

async def copy_to_clipboard(text):
    """Copy text to the system clipboard"""
    try:
        await asyncio.to_thread(pyperclip.copy, text)
        return {"success": True, "message": f"Copied to clipboard: {text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_copy_to_clipboard_tool():
    return {
        "name": "copy_to_clipboard",
        "description": "Copyt text to the system clipboard on user request. ",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The requested text to be copied to the clipboard."
                }
            },
            "required": ["text"]
        }
    }
