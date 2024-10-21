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

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/remove-bg")
async def remove_bg(image: bytes = None):
    if not image:
        return {"error": "No image provided."}

    input_img = Image.open(io.BytesIO(image))
    output_img = remove(input_img)

    buf = io.BytesIO()
    output_img.save(buf, format="PNG")
    buf.seek(0)

    return {"message": "Background removed successfully!"}

if __name__ == "__main__":
    # Get the dynamic port assigned by Render (default to 5000 if not set)
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
