import sys
import streamlit as st
import numpy as np
import torch
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import json
import base64
import io
import time

# Torch Model
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

def run_mnist_inference(image):
    print(image)
    image = Image.fromarray(image)
    image.save("test.png")
    # run processing steps

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((28, 28)),
        transforms.Normalize((0.1307,), (0.3081,)),  # Adjust the size as needed
    ])
    image = transform(image).unsqueeze(0)
    
    
    state_dict = torch.load('/home/tiny_ling/projects/potluckai/fast/mnist/mnist_mlp.pt')
    model = MLP()
    model.load_state_dict(state_dict=state_dict)
    model.eval()
    image = image.to("cuda")
    model.to("cuda")

    with torch.no_grad():
        output = model(image.view(-1, 784))
        output_list = output.cpu().numpy().tolist()[0]
        result = int(np.argmax(output_list))
        return result
   


# Streamlit UI
st.title("MNIST Digits Classification")
st.subheader("What is MNIST")
st.write("MNSIT is the famous digit classification task in deep learning. We try to input an image to a neural network and predict what digit it belongs to.")
col1, col2, col3 = st.columns(3)
col1.metric("Memory Usage", "10 MB", "1.2 °F")
col2.metric("Number of Params", "200", "-8%")
col3.metric("Top Accuracy", "96%")
st.write("How to classify MNIST digits with a neural network?")
st.subheader("Try it out")
col1, col2 = st.columns(2)
run_inference = False
with col1:
    st.write("Draw a number !")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=8,
        stroke_color="#FFFFFF",
        background_color="#000000",
        background_image=None,
        update_streamlit=True,
        height=150,
        width=150,
        drawing_mode="freedraw",
        point_display_radius=3,
        display_toolbar=True,
        key="full_app",
    )
    if st.button("Predict"):
        run_inference  = True

with col2:
    st.write("Our neural network predicts that it is a...")
    if canvas_result.image_data is not None and run_inference is True:
        if not np.allclose(canvas_result.image_data,np.zeros(canvas_result.image_data.shape)):
            with st.spinner('Wait for it...'):
                prediction = run_mnist_inference(canvas_result.image_data)
            run_inference = False
            st.write(f"Number {prediction}")
            st.success("Done!")

st.subheader("How does it all work?")
st.write()
# Do something interesting with the image data and paths
# if canvas_result.image_data is not None:
#     st.image(canvas_result.image_data)
