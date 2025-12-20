"""
FastAPI server for AnimateDiff video generation
Runs on port 8501 to match the expected VISION_API_URL
"""

import os
import json
import torch
import random
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from omegaconf import OmegaConf
from datetime import datetime

from diffusers import AutoencoderKL
from diffusers import DDIMScheduler, EulerDiscreteScheduler, PNDMScheduler
from diffusers.utils.import_utils import is_xformers_available
from transformers import CLIPTextModel, CLIPTokenizer

from animatediff.models.unet import UNet3DConditionModel
from animatediff.pipelines.pipeline_animation import AnimationPipeline
from animatediff.utils.util import save_videos_grid, load_weights, auto_download, MOTION_MODULES, BACKUP_DREAMBOOTH_MODELS

# Initialize FastAPI app
app = FastAPI(title="AnimateDiff API Server")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Device configuration
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🎬 AnimateDiff API Server - Using device: {device}")

# Default configuration
PRETRAINED_SD = "runwayml/stable-diffusion-v1-5"
default_motion_module = "v3_sd15_mm.ckpt"
default_inference_config = "configs/inference/inference-v3.yaml"
default_dreambooth_model = "realisticVisionV60B1_v51VAE.safetensors"

scheduler_dict = {
    "DDIM": DDIMScheduler,
    "Euler": EulerDiscreteScheduler,
    "PNDM": PNDMScheduler,
}

# Global pipeline controller (initialized on startup)
pipeline_controller = None


class VideoGenerationRequest(BaseModel):
    # Old format (for backward compatibility)
    prompt: Optional[str] = None
    negative_prompt: Optional[str] = "blurry, low quality, distorted, text, watermark"
    num_frames: Optional[int] = 16
    guidance_scale: Optional[float] = 7.5
    steps: Optional[int] = 25
    seed: Optional[int] = None
    fps: Optional[int] = 8
    
    # New comprehensive format
    title: Optional[str] = None
    level: Optional[str] = None
    duration: Optional[str] = None
    tts_enabled: Optional[bool] = None
    scenes: Optional[List[Dict[str, Any]]] = None
    prompts: Optional[List[str]] = None
    text: Optional[str] = None
    video_style: Optional[str] = None
    style_modifiers: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AnimateController:
    """Controller for AnimateDiff pipeline"""
    
    def __init__(self):
        self.basedir = os.getcwd()
        self.stable_diffusion_dir = os.path.join(self.basedir, "models", "StableDiffusion")
        self.motion_module_dir = os.path.join(self.basedir, "models", "Motion_Module")
        self.personalized_model_dir = os.path.join(self.basedir, "models", "DreamBooth_LoRA")
        self.pipeline = None
        
        # Create model directories if they don't exist
        os.makedirs(self.motion_module_dir, exist_ok=True)
        os.makedirs(self.personalized_model_dir, exist_ok=True)
        
        # Initialize pipeline (will download models automatically if needed)
        print("🎬 Initializing AnimateDiff pipeline...")
        print("   This may take several minutes on first run to download models...")
        self.update_pipeline(
            stable_diffusion_dropdown=PRETRAINED_SD,
            motion_module_dropdown=default_motion_module,
            base_model_dropdown=default_dreambooth_model,
            sampler_dropdown="DDIM",
        )
    
    def update_pipeline(
        self,
        stable_diffusion_dropdown=PRETRAINED_SD,
        motion_module_dropdown=default_motion_module,
        base_model_dropdown=default_dreambooth_model,
        lora_model_dropdown="none",
        lora_alpha_dropdown="0.6",
        sampler_dropdown="DDIM",
    ):
        """Update the animation pipeline with new models"""
        try:
            if "v2" in motion_module_dropdown:
                inference_config = "configs/inference/inference-v2.yaml"
            elif "v3" in motion_module_dropdown:
                inference_config = "configs/inference/inference-v3.yaml"
            else:
                inference_config = "configs/inference/inference-v1.yaml"

            print(f"🎬 Loading inference config: {inference_config}")
            unet = UNet3DConditionModel.from_pretrained_2d(
                stable_diffusion_dropdown, subfolder="unet", 
                unet_additional_kwargs=OmegaConf.load(inference_config).unet_additional_kwargs
            )
            
            if is_xformers_available() and torch.cuda.is_available():
                unet.enable_xformers_memory_efficient_attention()

            noise_scheduler_cls = scheduler_dict[sampler_dropdown]
            noise_scheduler_kwargs = OmegaConf.load(inference_config).noise_scheduler_kwargs
            
            if noise_scheduler_cls == EulerDiscreteScheduler:
                noise_scheduler_kwargs.pop("steps_offset", None)
                noise_scheduler_kwargs.pop("clip_sample", None)
            elif noise_scheduler_cls == PNDMScheduler:
                noise_scheduler_kwargs.pop("clip_sample", None)

            pipeline = AnimationPipeline(
                unet=unet,
                vae=AutoencoderKL.from_pretrained(stable_diffusion_dropdown, subfolder="vae"), 
                text_encoder=CLIPTextModel.from_pretrained(stable_diffusion_dropdown, subfolder="text_encoder"), 
                tokenizer=CLIPTokenizer.from_pretrained(stable_diffusion_dropdown, subfolder="tokenizer"), 
                scheduler=noise_scheduler_cls(**noise_scheduler_kwargs),
            )

            motion_module_path = os.path.join(self.motion_module_dir, motion_module_dropdown)
            dreambooth_model_path = os.path.join(self.personalized_model_dir, base_model_dropdown) if base_model_dropdown else ""
            lora_model_path = os.path.join(self.personalized_model_dir, lora_model_dropdown) if lora_model_dropdown != "none" else ""

            # Auto-download models if they don't exist
            if motion_module_path and not os.path.exists(motion_module_path):
                print(f"📥 Downloading motion module: {motion_module_dropdown}")
                auto_download(motion_module_path, is_dreambooth_lora=False)
            
            if dreambooth_model_path and not os.path.exists(dreambooth_model_path):
                print(f"📥 Downloading base model: {base_model_dropdown}")
                auto_download(dreambooth_model_path, is_dreambooth_lora=True)

            pipeline = load_weights(
                pipeline,
                motion_module_path=motion_module_path,
                dreambooth_model_path=dreambooth_model_path,
                lora_model_path=lora_model_path,
                lora_alpha=float(lora_alpha_dropdown),
            )

            pipeline.to(device)
            self.pipeline = pipeline
            print("✅ Pipeline loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading pipeline: {e}")
            raise
    
    @torch.no_grad()
    def generate_video(
        self,
        prompt: str,
        negative_prompt: str = "",
        num_inference_steps: int = 25,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512,
        video_length: int = 16,
        seed: Optional[int] = None,
    ) -> str:
        """Generate video and return file path"""
        if seed is not None and seed != -1:
            torch.manual_seed(seed)
        else:
            torch.seed()
        
        if not self.pipeline:
            raise RuntimeError("Pipeline not initialized")
        
        print(f"🎬 Generating video with prompt: {prompt[:50]}...")
        
        sample = self.pipeline(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            video_length=video_length,
        ).videos
        
        # Save to temporary file
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"animatediff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        save_videos_grid(sample, output_path)
        print(f"✅ Video saved to: {output_path}")
        
        return output_path


# Initialize controller on startup
@app.on_event("startup")
async def startup_event():
    global pipeline_controller
    print("🚀 Starting AnimateDiff API Server...")
    try:
        pipeline_controller = AnimateController()
        print("✅ AnimateDiff pipeline initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        print("⚠️  Server will start but video generation will fail until pipeline is initialized")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "device": device,
        "pipeline_loaded": pipeline_controller is not None and pipeline_controller.pipeline is not None
    }


@app.post("/generate-video")
async def generate_video(request: VideoGenerationRequest, x_api_key: Optional[str] = Header(None)):
    """
    Generate video using AnimateDiff
    Supports both old format (prompt-based) and new format (comprehensive video format)
    """
    try:
        if not pipeline_controller or not pipeline_controller.pipeline:
            raise HTTPException(status_code=503, detail="Pipeline not initialized. Please check server logs.")
        
        # Extract parameters from request
        if request.title and request.scenes and request.prompts:
            # New comprehensive format - combine prompts into single prompt
            combined_prompt = " ".join([
                p.get("text", "") if isinstance(p, dict) else str(p) 
                for p in request.prompts[:3]
            ])
            if not combined_prompt and request.text:
                combined_prompt = request.text[:500]
            
            # Use default values for video generation params
            prompt = combined_prompt
            negative_prompt = request.metadata.get("negative_prompt", "") if request.metadata else ""
            num_inference_steps = 25
            guidance_scale = 7.5
            width = 512
            height = 512
            video_length = 16
            seed = request.metadata.get("seed") if request.metadata else None
            
        elif request.prompt:
            # Old format
            prompt = request.prompt
            negative_prompt = request.negative_prompt or ""
            num_inference_steps = request.steps or 25
            guidance_scale = request.guidance_scale or 7.5
            width = 512
            height = 512
            video_length = request.num_frames or 16
            seed = request.seed
            
        elif request.text:
            # Text-only format
            prompt = request.text[:500]
            negative_prompt = ""
            num_inference_steps = 25
            guidance_scale = 7.5
            width = 512
            height = 512
            video_length = 16
            seed = None
        else:
            raise HTTPException(status_code=400, detail="No prompt, text, or scenes provided")
        
        if not prompt or len(prompt.strip()) == 0:
            raise HTTPException(status_code=400, detail="Prompt is empty")
        
        print(f"🎬 Generating video...")
        print(f"   Prompt: {prompt[:100]}...")
        print(f"   Steps: {num_inference_steps}, Guidance: {guidance_scale}, Length: {video_length}")
        
        # Generate video
        video_path = pipeline_controller.generate_video(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            video_length=video_length,
            seed=seed,
        )
        
        if not os.path.exists(video_path):
            raise HTTPException(status_code=500, detail="Video file was not created")
        
        # Return video file
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename="generated_video.mp4",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": f'attachment; filename="generated_video.mp4"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating video: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating video: {str(e)}")


@app.post("/test-generate-video")
async def test_generate_video(request: VideoGenerationRequest):
    """Test endpoint for video generation (no API key required)"""
    return await generate_video(request, x_api_key=None)


if __name__ == "__main__":
    import uvicorn
    print("🎬 Starting AnimateDiff API Server on port 8501...")
    print("🎬 Server will be available at: http://localhost:8501")
    print("🎬 API endpoint: http://localhost:8501/generate-video")
    print("🎬 Health check: http://localhost:8501/health")
    uvicorn.run(app, host="0.0.0.0", port=8501)
