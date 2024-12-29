
import asyncio
import pyautogui

async def output_text_to_screen(text: str):
    try:
        
        pyautogui.alert(text, "Message from Gemini")
        return {"success": True, "message": f"Outputted text: {text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_output_text_to_screen_tool():
    return {
        "name": "output_text_to_screen",
        "description": "Triggers output on the screen to display a message. Useful for displaying information to the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text content to be outputted on the screen."
                }
            },
            "required": ["text"]
        }
    }
if __name__ == '__main__':
    async def main():
        result = await output_text_to_screen("This is a test output.")
        print(result)
    asyncio.run(main())

