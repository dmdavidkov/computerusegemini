import asyncio
import base64
import io
import os
import sys
import traceback
import cv2
import pyaudio
import PIL.Image
import mss
import argparse
from google import genai
import websockets
from function_tools.function_hub import get_all_tools, execute_function
from dotenv import load_dotenv
load_dotenv(override=True)  # take environment variables from .env.

FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024
MODEL = "models/gemini-2.0-flash-exp"
DEFAULT_VIDEO_MODE = "screen"
DEFAULT_MODALITY = "AUDIO"
SYSTEM_INSTRUCTION = "For tasks that require multiple steps involving function calls, provide all the necessary function calls in a single response. Do not repeat what the user said or what you are going to do. Acknowledge if the function calls were successful."
print(os.getenv("GEMINI_API_KEY"))
client = genai.Client(http_options={"api_version": "v1alpha"}, api_key=os.getenv("GEMINI_API_KEY"))

CONFIGA = {"generation_config": {"response_modalities": ["AUDIO"], "temperature": 0},
          "system_instruction": SYSTEM_INSTRUCTION}
CONFIGT = {"generation_config": {"response_modalities": ["TEXT"], "temperature": 0},
          "system_instruction": SYSTEM_INSTRUCTION}

pya = pyaudio.PyAudio()

class AudioLoop:
    def __init__(self, video_mode=DEFAULT_VIDEO_MODE, modality=DEFAULT_MODALITY):
        self.video_mode = video_mode
        self.audio_in_queue = None
        self.out_queue = None
        self.session = None
        self.send_text_task = None
        self.receive_audio_task = None
        self.play_audio_task = None
        self.modality = modality

    def get_tools(self):
        return get_all_tools()

    async def handle_function_call(self, tool_calls):
        """Handle function calls from the model"""
        results = []
        for call in tool_calls:
            result = await execute_function(call.name, call.args)
            results.append(result)
        return results

    async def send_text(self):
        while True:
            text = await asyncio.to_thread(
                input,
                "message > ",
            )
            
            if text.lower() == "q":
                break

                
            await self.session.send(text or ".", end_of_turn=True)

    def _get_frame(self, cap):
        ret, frame = cap.read()
        if not ret:
            return None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(frame_rgb)
        img.thumbnail([1024, 1024])
        image_io = io.BytesIO()
        img.save(image_io, format="jpeg")
        image_io.seek(0)
        mime_type = "image/jpeg"
        image_bytes = image_io.read()
        return {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode()}

    async def get_frames(self):
        cap = await asyncio.to_thread(
            cv2.VideoCapture, 0
        )
        while True:
            frame = await asyncio.to_thread(self._get_frame, cap)
            if frame is None:
                break
            await asyncio.sleep(1.0)
            await self.out_queue.put(frame)
        cap.release()

    def _get_screen(self):
        sct = mss.mss()
        monitor = sct.monitors[0]
        i = sct.grab(monitor)
        mime_type = "image/jpeg"
        image_bytes = mss.tools.to_png(i.rgb, i.size)
        img = PIL.Image.open(io.BytesIO(image_bytes))
        image_io = io.BytesIO()
        img.save(image_io, format="jpeg")
        image_io.seek(0)
        image_bytes = image_io.read()
        return {"mime_type": mime_type, "data": base64.b64encode(image_bytes).decode()}

    async def get_screen(self):
        while True:
            frame = await asyncio.to_thread(self._get_screen)
            if frame is None:
                break
            await asyncio.sleep(1)
            await self.out_queue.put(frame)

    async def send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            await self.session.send(msg)

    async def listen_audio(self):
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )

        if __debug__:
            kwargs = {"exception_on_overflow": False}
        else:
            kwargs = {}

        while True:
            data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE, **kwargs)
            await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})

    async def receive_audio(self):
        while True:
            turn = self.session.receive()
            async for response in turn:
                
                # print the contents of response.tool_call if it exists
                # if response.tool_call or response.tool_call_cancellation:
                #     print(response.tool_call)
                #     print(response.tool_call_cancellation)

                if tool_call := response.tool_call:
                    result = await self.handle_function_call(tool_call.function_calls)

                    tool_responses = genai.types.LiveClientToolResponse(
                        function_responses=[
                            genai.types.FunctionResponse(
                                id=call.id,
                                name=call.name,
                                response={'result': result[i]}
                            ) for i, call in enumerate(tool_call.function_calls)
                        ]
                    )
                    
                    await self.session.send(tool_responses)
                    
                if data := response.data:
                    self.audio_in_queue.put_nowait(data)
                    continue
                if text := response.text:
                    print(text, end="")

            while not self.audio_in_queue.empty():
                self.audio_in_queue.get_nowait()

    async def play_audio(self):
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        while True:
            bytestream = await self.audio_in_queue.get()
            await asyncio.to_thread(stream.write, bytestream)

    async def run(self):
        while True:
            try:
                if self.modality == "AUDIO":
                    config = CONFIGA.copy()
                else:
                    config = CONFIGT.copy()

                config["tools"] = self.get_tools()
                async with (
                    client.aio.live.connect(model=MODEL, config=config) as session,
                    asyncio.TaskGroup() as tg,
                ):
                    self.session = session
                    self.audio_in_queue = asyncio.Queue()
                    self.out_queue = asyncio.Queue(maxsize=5)
                    send_text_task = tg.create_task(self.send_text())
                    tg.create_task(self.send_realtime())
                    tg.create_task(self.listen_audio())
                    if self.video_mode == "camera":
                        tg.create_task(self.get_frames())
                    elif self.video_mode == "screen":
                        tg.create_task(self.get_screen())
                    tg.create_task(self.receive_audio())
                    tg.create_task(self.play_audio())
                    await send_text_task
                    raise asyncio.CancelledError("User requested exit")
                
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed: {e}, retrying in 3 seconds...")
                await asyncio.sleep(3)
                continue
            except asyncio.CancelledError:
                pass
            except ExceptionGroup as EG:
                self.audio_stream.close()
                traceback.print_exception(EG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        default=DEFAULT_VIDEO_MODE,
        help="pixels to stream from",
        choices=["camera", "screen", "none"],
    )
    parser.add_argument(
        "--modality",
        type=str,
        default=DEFAULT_MODALITY,
        help="modality to use",
        choices=["AUDIO", "TEXT"],
    )
    args = parser.parse_args()
    main = AudioLoop(video_mode=args.mode, modality=args.modality)
    asyncio.run(main.run())
