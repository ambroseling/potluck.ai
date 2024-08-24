import asyncio
from fastapi import FastAPI, WebSocket, File, UploadFile, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import json
import sys
sys.path.append("/home/tiny_ling/projects/2bros2gpus")

import base64
import numpy as np
import redis
import asyncio

#https://medium.com/distributed-computing-with-ray/how-to-scale-up-your-fastapi-application-using-ray-serve-c9a7b69e786

class ConnectionManager:
    def __init__(self):
        self.active_connections = []
    async def create_connection(self,websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def remove_connection(self,websocket:WebSocket):
        self.active_connections.remove(websocket)
    async def handle_inference_request(self,websocket):
        pass
    async def handle_broadcast(self,message:str):
        pass
    async def get_gpu_memory_usage(self):
        import GPUtil
        gpus = GPUtil.getGPUs()
        while True:
            for connection in self.active_connections:
                await connection.send_json({"gpu_memory_usage": {gpu.id: gpu.memoryUtil for gpu in gpus} })
                await asyncio.sleep(1)   

app = FastAPI()

manager = ConnectionManager()

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)


# async def mnist(image: str, websocket: WebSocket):
#     # Decode base64 image data


#     # run model inference logic
#     await run_mnist_inference(image,websocket)
    

# async def opensora(prompt:str, sampling_steps:int, sampler:str ,websocket:WebSocket):
#     await run_sora_inference(text_prompt=prompt, sampling_steps=sampling_steps, sampler=sampler ,websocket=websocket)
#     # read the text
#     # send to sora
#     # get the video
#     # send it back through web socket
    

# async def mistral (prompt:str,websocket:WebSocket):
#     await run_mistral_inference(prompt,websocket)


# async def switch(data,websocket):
#     payload = json.loads(data)
#     print(payload)
#     config = payload.get("config")

#     if config == "mnist":
#         if 'image' in payload:
#             2    
#             image_b64 = payload.get("image")
#         await mnist(websocket=websocket,image = image_b64)
#     elif config == "sora":
#         if "prompt" in payload:
#             prompt = payload.get("prompt")
#         if "sampling_steps" in payload:
#             sampling_steps = payload.get("sampling_steps")
#         if "sampler" in payload:
#             sampler = payload.get("sampler")
#         await opensora(prompt = prompt, sampling_steps = sampling_steps, sampler=sampler,websocket=websocket)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket,client_id:int):
    await manager.create_connection(websocket=websocket)
    try:
          while True:
            manager.get_gpu_memory_usage()
    except WebSocketDisconnect:
        await manager.remove_connection(websocket=websocket)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(manager.get_gpu_memory_usage())



