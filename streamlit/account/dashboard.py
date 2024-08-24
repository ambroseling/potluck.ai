import streamlit as st
import torch
import time
import nvsmi
from streamlit_card import card


st.set_page_config(
    page_title="potluck.ai",
    page_icon="🍲",
    layout="wide",
)
st.title("Explore ")
st.write("We created a platform for people to share their ideas, weights and code in ML. This will also be a platform for Ambrose and Ali to house their Machine Learning Content.")
st.write("Pick a ML model you find interesting and run it with our GPUs! We try to also cover what we know about the models and how they work, let us know if you find it helpful or if you have any comments on the technical details!")

_, ambrose_gpu_total = torch.cuda.mem_get_info(torch.cuda.current_device())

@st.fragment(run_every="2s")
def gpus():
    for gpu in nvsmi.get_gpus():
        ambrose_gpu_free = gpu.mem_free
    col1,col2 = st.columns(2)
    col1.metric("Ali's GPU :sunglasses:", "10 MB", f"out of 100MB")
    col2.metric("Ambrose's GPU",f"{(ambrose_gpu_free):.2f} MB",f"out of {(ambrose_gpu_total/1e9):.4f} GB")
gpus()

st.subheader("Latest Releases & Trending")
st.divider()
with st.container():
    first,second_first,_,_,_,_,second_last,last = st.columns(8,vertical_alignment="center")
    with first:
        st.markdown('''
                    <a href="https://ibb.co/yQk7gYc">
                    <img src="https://i.ibb.co/kgYrk4F/mnist.jpg" alt="resnet" style="width:50%; height:auto; border-radius:15px;" border="0">
                    </a>
                    ''',unsafe_allow_html =True)
    with second_first:
        st.write("classify some hand-written digits using a neural network")
    with second_last:
        st.write("5MB")
    with last:
        with st.container():
            st.button("Try it out!",key="try1")
            st.button(":material/favorite:",key="fav1")
        
st.divider()
with st.container():
    first,second_first,_,_,_,_,second_last,last = st.columns(8,vertical_alignment="center")
    with first:
        st.markdown('''
                    <a href="https://ibb.co/yQk7gYc">
                    <img src="https://i.ibb.co/Kwd4ZPG/tweet.jpg" alt="resnet" style="width:50%; height:auto; border-radius:15px;" border="0">
                    </a>
                    ''',unsafe_allow_html =True)
    with second_first:
        st.write("analyze some of trumpts tweets using recurrent neural networks")
    with second_last:
        st.write("10MB")
    with last:
        with st.container():
            st.button("Try it out!",key="try2")
            st.button(":material/favorite:",key="fav2")
st.divider()
with st.container():
    first,second_first,_,_,_,_,second_last,last = st.columns(8,vertical_alignment="center")
    with first:
        st.markdown('''
                    <a href="https://ibb.co/yQk7gYc">
                    <img src="https://i.ibb.co/pLK54RB/resnet.jpg" alt="resnet" style="width:50%; height:auto; border-radius:15px;" border="0">
                    </a>
                    ''',unsafe_allow_html =True)
    with second_first:
        st.write("doing object detection with a resnet transformer")
    with second_last:
        st.write("1GB")
    with last:
        with st.container():
            st.button("Try it out!",key="try3")
            st.button(":material/favorite:",key="fav3")
st.divider()
with st.container():
    first,second_first,_,_,_,_,second_last,last = st.columns(8,vertical_alignment="center")
    with first:
        st.markdown('''
                    <a href="https://ibb.co/yQk7gYc">
                    <img src="https://i.ibb.co/2ZDt3nh/ece-bot.jpg" alt="resnet" style="width:50%; height:auto; border-radius:15px;" border="0">
                    </a>
                    ''',unsafe_allow_html =True)
    with second_first:
        st.write("finetuning a gpt model to teach ece")
    with second_last:
        st.write("12GB")
    with last:
        with st.container():
            st.button("Try it out!",key="try4")
            st.button(":material/favorite:",key="fav4")
st.divider()

with st.container():
    first,second_first,_,_,_,_,second_last,last = st.columns(8,vertical_alignment="center")
    with first:
        st.markdown('''
                    <a href="https://ibb.co/yQk7gYc">
                    <img src="https://i.ibb.co/6XXvhHZ/youtubot.jpg" alt="resnet" style="width:50%; height:auto; border-radius:15px;" border="0">
                    </a>
                    ''',unsafe_allow_html =True)
    with second_first:
        st.write("a youtuber powered by gpt,sd,whisper,bark")
    with second_last:
        st.write("18GB")
    with last:
        with st.container():
            st.button("Try it out!",key="try5")
            st.button(":material/favorite:",key="fav5")


st.subheader("Your Favourites")


st.subheader("Your Models")


