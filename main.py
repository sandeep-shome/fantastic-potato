import os
import uvicorn
from fastapi import FastAPI
from PIL import Image
import io
from rembg import remove

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server is running."}

@app.get("/healthz")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get the dynamic port assigned by Render (default to 5000 if not set)
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
