import os
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server is running."}

@app.get("/healthz")
def health():
    return {"status": "healthy"}

# Compress image helper function
def compress_image(image: Image.Image, quality: int = 85) -> io.BytesIO:
    buf = io.BytesIO()
    image.save(buf, format="JPEG", optimize=True, quality=quality)
    buf.seek(0)
    return buf

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    # Validate if the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")

    # Open the uploaded image
    input_image = Image.open(file.file)

    # Step 1: Compress the image
    compressed_image_buf = compress_image(input_image)

    # Step 2: Remove background using `rembg`
    compressed_image = Image.open(compressed_image_buf)
    output_image = remove(compressed_image)

    # Save the output image to a buffer
    output_buf = io.BytesIO()
    output_image.save(output_buf, format="PNG")
    output_buf.seek(0)

    # Return the processed image as a response
    return StreamingResponse(output_buf, media_type="image/png")


if __name__ == "__main__":
    # Get the dynamic port assigned by Render (default to 5000 if not set)
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
