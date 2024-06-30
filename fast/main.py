import asyncio
from fastapi import FastAPI, WebSocket, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import json
from mnist.inference import run_mnist_inference, run_mnist_preprocessing
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
    await websocket.send_text("Processing your ugly handwriting...")

    # run model inference logic
    await run_mnist_inference(image,websocket)

    await websocket.send_text("Inference Complete")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            text_data = payload.get("text")
            image_b64 = payload.get("image")
            if text_data == "mnist":
                await mnist(websocket=websocket,image = image_b64)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()