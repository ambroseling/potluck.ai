import math
import os
import torch
import argparse
import torchvision
import os, sys
import json
import base64
sys.path.append('/home/tiny_ling/projects/2bros2gpus/fast/opensora/Open-Sora-Plan')
sys.path.append('/home/tiny_ling/projects/2bros2gpus/fast/opensora/Open-Sora-Plan/opensora/sample')
from diffusers.schedulers import (DDIMScheduler, DDPMScheduler, PNDMScheduler,
                                  EulerDiscreteScheduler, DPMSolverMultistepScheduler,
                                  HeunDiscreteScheduler, EulerAncestralDiscreteScheduler,
                                  DEISMultistepScheduler, KDPM2AncestralDiscreteScheduler)
from diffusers.schedulers.scheduling_dpmsolver_singlestep import DPMSolverSinglestepScheduler
from diffusers.models import AutoencoderKL, AutoencoderKLTemporalDecoder
from omegaconf import OmegaConf
from torchvision.utils import save_image
from transformers import T5EncoderModel, T5Tokenizer, AutoTokenizer
from opensora.models.ae import ae_stride_config, getae, getae_wrapper
from opensora.models.ae.videobase import CausalVQVAEModelWrapper, CausalVAEModelWrapper
from opensora.models.diffusion.latte.modeling_latte import LatteT2V
from opensora.models.text_encoder import get_text_enc
from opensora.utils.utils import save_video_grid
from pipeline_videogen import VideoGenPipeline
import imageio
from fastapi import FastAPI, WebSocket, File, UploadFile


def run_sora_inference(text_prompt:str, sampling_steps:int, sampler:str ):
    model_path = "/home/tiny_ling/projects/2bros2gpus/fast/opensora/Open-Sora-Plan-v1.1.0"
    version = "65x512x512"
    num_frames = 65
    height = 512
    width = 512
    cache_dir = "./cache_dir"
    text_encoder_name = "/home/tiny_ling/projects/2bros2gpus/fast/opensora/t5-v1_1-xxl"
    ae = "CausalVAEModel_4x8x8"
    ae_path = "/home/tiny_ling/projects/2bros2gpus/fast/opensora/Open-Sora-Plan-v1.1.0/vae"
    save_img_path = "./sample_video_65x512x512"
    fps = 24
    guidance_scale = 7.5
    num_sampling_steps = sampling_steps
    enable_tiling = True
    force_images = False
    sample_method = sampler
    run_time = 0
    tile_overlap_factor = 0.25

    torch.set_grad_enabled(False)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    vae = getae_wrapper(ae)(model_path, subfolder="vae", cache_dir=cache_dir).to(device, dtype=torch.float16)
    # vae = getae_wrapper(ae)(ae_path).to(device, dtype=torch.float16)
    if enable_tiling:
        vae.vae.enable_tiling()
        vae.vae.tile_overlap_factor = tile_overlap_factor
    vae.vae_scale_factor = ae_stride_config[ae]
    # Load model:
    transformer_model = LatteT2V.from_pretrained(model_path, subfolder=version, cache_dir=cache_dir, torch_dtype=torch.float16).to(device)
    # transformer_model = LatteT2V.from_pretrained(model_path, low_cpu_mem_usage=False, device_map=None, torch_dtype=torch.float16).to(device)
    
    transformer_model.force_images = force_images
    tokenizer = T5Tokenizer.from_pretrained(text_encoder_name, cache_dir=cache_dir)
    text_encoder = T5EncoderModel.from_pretrained(text_encoder_name, cache_dir=cache_dir, load_in_4bit= True, torch_dtype=torch.float16)

    if force_images:
        ext = 'jpg'
    else:
        ext = 'mp4'

    # set eval mode
    transformer_model.eval()
    vae.eval()
    text_encoder.eval()

    if sample_method == 'DDIM':  #########
        scheduler = DDIMScheduler()
    elif sample_method == 'EulerDiscrete':
        scheduler = EulerDiscreteScheduler()
    elif sample_method == 'DDPM':  #############
        scheduler = DDPMScheduler()
    elif sample_method == 'DPMSolverMultistep':
        scheduler = DPMSolverMultistepScheduler()
    elif sample_method == 'DPMSolverSinglestep':
        scheduler = DPMSolverSinglestepScheduler()
    elif sample_method == 'PNDM':
        scheduler = PNDMScheduler()
    elif sample_method == 'HeunDiscrete':  ########
        scheduler = HeunDiscreteScheduler()
    elif sample_method == 'EulerAncestralDiscrete':
        scheduler = EulerAncestralDiscreteScheduler()
    elif sample_method == 'DEISMultistep':
        scheduler = DEISMultistepScheduler()
    elif sample_method == 'KDPM2AncestralDiscrete':  #########
        scheduler = KDPM2AncestralDiscreteScheduler()
    print('videogen_pipeline', device)
    videogen_pipeline = VideoGenPipeline(vae=vae,
                                         text_encoder=text_encoder,
                                         tokenizer=tokenizer,
                                         scheduler=scheduler,
                                         transformer=transformer_model)
    
    # videogen_pipeline.enable_xformers_memory_efficient_attention()
    if not os.path.exists(save_img_path):
        os.makedirs(save_img_path)

    video_grids = []
    if not isinstance(text_prompt, list):
        text_prompt = [text_prompt]
    if len(text_prompt) == 1 and text_prompt[0].endswith('txt'):
        text_prompt = open(text_prompt[0], 'r').readlines()
        text_prompt = [i.strip() for i in text_prompt]
    
    for idx, prompt in enumerate(text_prompt):    
        print('Processing the ({}) prompt'.format(prompt))
        videos = videogen_pipeline(prompt,
                                   num_frames=num_frames,
                                   width=width,
                                   height=height,
                                   num_inference_steps=num_sampling_steps,
                                   guidance_scale=guidance_scale,
                                   enable_temporal_attentions=not force_images,
                                   num_images_per_prompt=1,
                                   mask_feature=True,
                                   )
        videos = videos.video
        print(videos.shape)
        try:
            if force_images:
                videos = videos[:, 0].permute(0, 3, 1, 2)  # b t h w c -> b c h w
                save_image(videos / 255.0, os.path.join(save_img_path, f'{idx}.{ext}'),
                           nrow=1, normalize=True, value_range=(0, 1))  # t c h w
                

            else:
                imageio.mimwrite(
                    os.path.join(
                        save_img_path, f'{idx}.{ext}'), videos[0],
                    fps=fps, quality=9)  # highest quality is 10, lowest is 0
        except:
            print('Error when saving {}'.format(prompt))
        video_grids.append(videos)
    video_grids = torch.cat(video_grids, dim=0)
    video_path = os.path.join(save_img_path, f'{idx}.{ext}')

    if os.path.exists(video_path):
        with open(video_path, "rb") as video_file:
            video_data = video_file.read()
            encoded_video = base64.b64encode(video_data).decode('utf-8')
            print("Encoding the video...")
        return encoded_video
    else:
        return -1

    # # torchvision.io.write_video(save_img_path + '_%04d' % run_time + '-.mp4', video_grids, fps=6)
    # if force_images:
    #     save_image(video_grids / 255.0, os.path.join(save_img_path, f'{sample_method}_gs{guidance_scale}_s{num_sampling_steps}.{ext}'),
    #                nrow=math.ceil(math.sqrt(len(video_grids))), normalize=True, value_range=(0, 1))
    # else:
    #     video_grids = save_video_grid(video_grids)
    #     # imageio.mimwrite(os.path.join(save_img_path, f'{sample_method}_gs{guidance_scale}_s{num_sampling_steps}.{ext}'), video_grids, fps=fps, quality=9)

if __name__ == "__main__":
    text_prompt = "A ferrari going super fast"
    run_sora_inference(text_prompt=text_prompt)