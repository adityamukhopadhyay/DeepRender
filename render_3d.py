import os
import fal_client
import base64
from PIL import Image
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get FAL API key from environment variables
FAL_KEY = os.getenv("FAL_KEY")
if not FAL_KEY:
    raise ValueError("FAL_KEY not found in environment variables. Please check your .env file.")

def on_queue_update(update):
    """Handle queue updates and log messages"""
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

def image_to_3d(image_path, output_path="output.glb"):
    # Configure FAL client
    fal_client.api_key = FAL_KEY

    # Load and encode image
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()
        img_b64 = base64.b64encode(img_data).decode()
        img_uri = f"data:image/jpeg;base64,{img_b64}"

    # Call Trellis API
    print("Starting 3D model generation...")
    
    # Submit the request
    handler = fal_client.submit(
        "fal-ai/trellis",
        arguments={
            "image_url": img_uri,
            "ss_guidance_strength": 7.5,
            "ss_sampling_steps": 12,
            "slat_guidance_strength": 3,
            "slat_sampling_steps": 12,
            "mesh_simplify": 0.95,
            "texture_size": 1024
        }
    )
    
    # For better texture quality use:
    '''arguments={
        "image_url": img_uri,
        "slat_guidance_strength": 5,     # Increased for better texture accuracy
        "slat_sampling_steps": 20,       # Increased for more texture detail
        "texture_size": 2048,            # Increased for higher resolution textures
        "ss_guidance_strength": 7.5,
        "ss_sampling_steps": 12,
        "mesh_simplify": 0.95
    }'''
    # For better shape quality use:
    '''arguments={
        "image_url": img_uri,
        "ss_guidance_strength": 10,      # Increased for better shape accuracy
        "ss_sampling_steps": 20,         # Increased for more shape detail
        "mesh_simplify": 0.98,           # Increased for more geometric detail
        "slat_guidance_strength": 3,
        "slat_sampling_steps": 12,
        "texture_size": 1024
    }'''
    
    request_id = handler.request_id
    print(f"Request ID: {request_id}")

    # Check status and wait for completion
    while True:
        status = fal_client.status("fal-ai/trellis", request_id, with_logs=True)
        if hasattr(status, 'logs'):
            for log in status.logs:
                print(log["message"])
        if not isinstance(status, fal_client.InProgress):
            break

    # Get the final result
    result = fal_client.result("fal-ai/trellis", request_id)

    # Save the 3D model
    if isinstance(result, dict) and result.get("model_mesh"):
        model_url = result["model_mesh"]["url"]
        
        # Download the model
        response = requests.get(model_url)
        response.raise_for_status()
        
        # Save the model
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        print(f"3D model saved to {output_path}")
        return output_path
    else:
        raise Exception("Failed to generate 3D model")

if __name__ == "__main__":
    # Replace with your image path
    input_image = "sample.jpg"  # Make sure this image exists in the same directory
    output_file = "output.glb"
    
    try:
        model_path = image_to_3d(input_image, output_file)
        print(f"Successfully created 3D model at: {model_path}")
    except Exception as e:
        print(f"Error: {str(e)}") 