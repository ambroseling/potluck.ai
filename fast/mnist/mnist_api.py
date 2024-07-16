import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import json
from fastapi import FastAPI, WebSocket, File, UploadFile

class MLP(nn.Module):
    def __init__(self, hidden_size_1=100, hidden_size_2=100):
        super(MLP,self).__init__()
        self.linear1 = nn.Linear(28*28, hidden_size_1) 
        self.linear2 = nn.Linear(hidden_size_1, hidden_size_2) 
        self.linear3 = nn.Linear(hidden_size_2, 10)
        self.relu = nn.ReLU()

    def forward(self, img):
        x = img.view(-1, 28*28)
        x = self.relu(self.linear1(x))
        x = self.relu(self.linear2(x))
        x = self.linear3(x)
        return x

def validate_mnist_logging(data):
    if "message" in data and isinstance(data["message"], str):
        return True
    else:
        return False


def validate_mnist_result(data):
    if "probabilities" in data and isinstance(data["probabilities"], list) and "message" in data and isinstance(data["message"], str):
        return True
    return False

def run_mnist_preprocessing(image:Image):
    # Initialize PyTorch transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((28, 28)),
        transforms.Normalize((0.1307,), (0.3081,)),  # Adjust the size as needed
    ])
    tensor_image = transform(image).unsqueeze(0)  # Add batch dimension    await websocket.send_text("Image received and processing started.")
    return tensor_image

async def run_mnist_inference(image:torch.Tensor,websocket:WebSocket):
    state_dict = torch.load('mnist/mnist_mlp.pt')
    model = MLP()
    model.load_state_dict(state_dict=state_dict)
    result = {"message": "Loading the model.."}
    if validate_mnist_logging(result):
        await websocket.send_text(json.dumps(result))
    else:
        await websocket.send_text(json.dumps({"error": "Invalid data format"}))    


    model.eval()
    image = image.to("cuda")
    model.to("cuda")

    result = {"message": "Model is on the GPU and running..."}
    if validate_mnist_logging(result):
        await websocket.send_text(json.dumps(result))
    else:
        await websocket.send_text(json.dumps({"error": "Invalid data format"}))    

    with torch.no_grad():
        output = model(image.view(-1, 784))
        output_list = output.cpu().numpy().tolist()[0]
        result = {"probabilities": output_list, "message": "Inference completed"}
        if validate_mnist_result(result):
            await websocket.send_text(json.dumps(result))
        else:
            await websocket.send_text(json.dumps({"error": "Invalid data format"}))    
