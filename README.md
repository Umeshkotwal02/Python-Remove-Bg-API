# Background Removal Backend

## Setup
This backend uses Python. It attempts to use `rembg` (Standard) or `transparent-background` (Fallback) for background removal.

### Prerequisites
- Python 3.10, 3.11, or 3.12 is recommended.
- Python 3.14 (your current version) has limited support for AI libraries (OnnxRuntime missing).

### Installation
1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   If `rembg` fails to install (on Python 3.14+), try installing the fallback:
   ```bash
   pip install transparent-background flask flask-cors pillow waitress
   ```

### Running the Server
```bash
python main.py
```
The server will run on `http://localhost:5000`.

## API Endpoint
**POST** `/remove-bg`
- **Body**: form-data with key `image` (file).
- **Response**: PNG image.
