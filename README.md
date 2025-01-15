# DeepRender

Convert 2D images to textured 3D models using AI. This tool allows you to generate 3D models (.glb) from single images, complete with textures and geometry.

## Features
- Single image to 3D model conversion
- Textured 3D model output in GLB format
- Configurable quality settings for shape and texture
- Progress tracking during model generation

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-repo/deeprender.git
cd deeprender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your FAL API key:
```bash
FAL_KEY=your_fal_api_key
```

4. Run the script:
Place your source image in the project directory as `sample.jpg`

```bash
python render_3d.py
```
5. The 3D model will be saved as `output.glb`

## Configuration Options

The script supports different quality settings:

### For Better Texture Quality:
```bash
arguments = {
    "slat_guidance_strength": 5, # Increased texture accuracy
    "slat_sampling_steps": 20, # More texture detail
    "texture_size": 2048, # Higher resolution textures
    "mesh_simplify": 0.95
}
```

### For Better Shape Quality:
```bash
arguments = {
    "ss_guidance_strength": 10, # Better shape accuracy
    "ss_sampling_steps": 20, # More shape detail
    "mesh_simplify": 0.98, # More geometric detail
    "texture_size": 1024
}
```

## Limitations & Post-Processing

### Material Properties
When converting 2D images to 3D models, certain material properties cannot be automatically determined from a single image. This includes:
- Transparency
- Reflectivity
- Refraction
- Surface properties (like glass or metallic surfaces)

This is a fundamental limitation of single-image 3D reconstruction, as these properties require additional information that isn't available in a 2D image.

### Handling Transparent Objects
For objects that should be transparent (like glasses, windows, or clear plastics), post-processing in 3D software is required:

1. Open the GLB file in Blender
2. Select the mesh parts that should be transparent
3. In the Material Properties:
   - Set Blend Mode to "Alpha Blend"
   - Adjust Transparency value
   - Add Glass BSDF shader
   - Configure refraction index (typically 1.45-1.52 for glasses)
   - Add reflection properties as needed

This post-processing step allows you to achieve realistic material properties that cannot be automatically inferred from the source image.

## Requirements
- Python 3.7+
- FAL API key from [fal.ai](https://fal.ai)
- Blender (optional, for post-processing materials)

## Error Handling
The script includes error handling for common issues:
- Missing API key
- Invalid image files
- Network connectivity issues
- API response errors

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.