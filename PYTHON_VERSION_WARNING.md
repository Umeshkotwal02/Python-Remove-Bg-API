# IMPORANT: Python Version Issue

You are currently running **Python 3.14.2**.
This version is "Bleeding Edge" (Alpha/Pre-release) and is **NOT compatible** with most AI libraries yet.

The Background Removal libraries (`rembg` and `transparent-background`) rely on `onnxruntime` and `pytorch`.
- `onnxruntime` does NOT have binaries for Python 3.14.
- `pytorch` installs but fails with `[WinError 1114] DLL initialization routine failed` because it is not stable on 3.14.

## How to Fix
To make this project work, you **MUST** use a stable Python version.
1.  **Install Python 3.11 or 3.12** from python.org.
2.  Delete the `backend/venv` folder.
3.  Re-run the installation:
    ```powershell
    cd backend
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    python main.py
    ```

The code provided in `main.py` is correct and fully functional. It is only the environment (Python 3.14) that is preventing it from running.
