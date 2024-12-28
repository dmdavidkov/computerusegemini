import asyncio
import logging
from .copy_to_clipboard import copy_to_clipboard, get_copy_to_clipboard_tool
from .copy_and_paste import input_text_to_screen, get_input_text_to_screen_tool
from .press_keys import press_keys, get_press_keys_tool
from .get_clipboard import get_clipboard, get_get_clipboard_tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

_TOOLS = {
    "copy_to_clipboard": {
        "function": copy_to_clipboard,
        "tool_data": get_copy_to_clipboard_tool()
    },
    "input_text_to_screen": {
        "function": input_text_to_screen,
        "tool_data": get_input_text_to_screen_tool()
    },
    "press_keys": {
        "function": press_keys,
        "tool_data": get_press_keys_tool()
    },
    "get_clipboard": {
        "function": get_clipboard,
        "tool_data": get_get_clipboard_tool()
    }
}

def get_all_tools():
    return [{"function_declarations": [tool_data["tool_data"] for tool_data in _TOOLS.values()]},
            {"code_execution": {}},
            {"google_search": {}}]

async def execute_function(name, args):
    logging.info(f"Calling function: {name} with args: {args}")
    if name not in _TOOLS:
        error_message = f"Unknown function: {name}"
        logging.error(error_message)
        return {"success": False, "error": error_message}
    result = await _TOOLS[name]["function"](**args)
    logging.info(f"Function {name} returned: {result}")
    return result
