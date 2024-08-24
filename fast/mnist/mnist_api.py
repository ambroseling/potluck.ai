import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import json
import base64
import io
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

async def run_mnist_inference(image:str):
    image_data = base64.b64decode(image.split(',')[1])  # Split off the data URL prefix

    # Convert image data to PIL Image object
    image = Image.open(io.BytesIO(image_data))
    new_image = Image.new("RGBA", image.size, "WHITE") # Create a white rgba background
    new_image.paste(image, (0, 0), image)  
    new_image = new_image.convert('RGB').convert('L')
    # run processing steps

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((28, 28)),
        transforms.Normalize((0.1307,), (0.3081,)),  # Adjust the size as needed
    ])
    image = transform(image).unsqueeze(0)
    
    
    state_dict = torch.load('mnist/mnist_mlp.pt')
    model = MLP()
    model.load_state_dict(state_dict=state_dict)
    model.eval()
    image = image.to("cuda")
    model.to("cuda")

    with torch.no_grad():
        output = model(image.view(-1, 784))
        output_list = output.cpu().numpy().tolist()[0]
        result = {"probabilities": output_list, "message": "Inference completed"}
        return result
   