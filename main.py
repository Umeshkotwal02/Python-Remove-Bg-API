from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
import os
from PIL import Image

# Initialize Backend
BACKEND = 'none'
BACKEND_ERROR = None

# Increase default timeout for AI processing
# Note: On shared hosting, execution time is often limited (e.g. 60s or 120s).
# If the image takes too long, the server will kill it.

try:
    # Try loading the SOTA model (InSPyReNet) via transparent-background first
    # This is much more robust for "camouflaged" images (same color fg/bg)
    from transparent_background import Remover
    # fast=True uses MobileNetV3 (faster, good accuracy)
    # fast=False uses ResNet50 (slower, best accuracy). 
    # Let's use fast=True first, it is usually better than rembg.
    remover = Remover(mode='base', fast=True) 
    BACKEND = 'transparent-background'
    print("AI Engine: transparent-background (InSPyReNet) loaded successfully")
except Exception as e:
    print(f"DEBUG: Failed to load transparent-background: {e}")
    TB_ERROR = str(e)
    try:
        from rembg import remove, new_session
        bg_session = new_session("u2net_human_seg") # Try human segmentation model as fallback
        BACKEND = 'rembg'
        print("AI Engine: rembg (u2net_human_seg) loaded as fallback")
    except Exception as e:
        BACKEND_ERROR = f"Transparent-Bg Error: {TB_ERROR} || Rembg Error: {e}"
        BACKEND = 'none'

app = Flask(__name__)
# Enable CORS for all domains or specify your frontend domain in production
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return f"Backend is running! Active Engine: {BACKEND}"

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    global BACKEND_ERROR
    
    if BACKEND == 'none':
        error_msg = 'No AI library installed. '
        if BACKEND_ERROR:
            error_msg += f"Debug Info: {BACKEND_ERROR}. "
        error_msg += "Please check server logs or install 'rembg'."
        return jsonify({'error': error_msg}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        input_image = Image.open(file.stream).convert("RGB")
        
        # Limit image size to prevent RAM overflow on shared hosting
        # Resizing to max 1080px (preserving aspect ratio)
        input_image.thumbnail((1080, 1080)) 
        
        if BACKEND == 'transparent-background':
            output_image = remover.process(input_image, type='rgba')
        elif BACKEND == 'rembg':
            output_image = remove(input_image, session=bg_session)
        
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': f"Processing failed: {str(e)}"}), 500

if __name__ == '__main__':
    # For local dev
    app.run(host='0.0.0.0', port=5000, debug=True)
