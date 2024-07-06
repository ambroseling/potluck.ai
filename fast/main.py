import asyncio
from fastapi import FastAPI, WebSocket, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import json
import sys
sys.path.append("/home/tiny_ling/projects/2bros2gpus")
from fast.mnist.mnist_api import run_mnist_inference, run_mnist_preprocessing
from fast.opensora.opensora_api import run_sora_inference
import base64
import numpy as np

app = FastAPI()


# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)


async def mnist(image: str, websocket: WebSocket):
    # Decode base64 image data
    image_data = base64.b64decode(image.split(',')[1])  # Split off the data URL prefix

    # Convert image data to PIL Image object
    image = Image.open(io.BytesIO(image_data))
    new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
    new_image.paste(image, (0, 0), image)  
    new_image = new_image.convert('RGB').convert('L')
    # run processing steps
    image = run_mnist_preprocessing(new_image)

    # run model inference logic
    await run_mnist_inference(image,websocket)
    

async def opensora(prompt:str, sampling_steps:int, sampler:str ,websocket:WebSocket):
    # read the text
    # send to sora
    # get the video
    # send it back through web socket
    await run_sora_inference(text_prompt=prompt, sampling_steps=sampling_steps, sampler=sampler ,websocket=websocket)
    




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            print(payload)
            config = payload.get("config")
            if config == "mnist":
                if 'image' in payload:
                    image_b64 = payload.get("image")
                await mnist(websocket=websocket,image = image_b64)
            elif config == "sora":
                if "prompt" in payload:
                    prompt = payload.get("prompt")
                if "sampling_steps" in payload:
                    sampling_steps = payload.get("sampling_steps")
                if "sampler" in payload:
                    sampler = payload.get("sampler")
                await opensora(prompt = prompt, sampling_steps = sampling_steps, sampler=sampler,websocket=websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()