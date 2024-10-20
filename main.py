from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image
import io
from rembg import remove

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server is running."}

@app.get("/health")
def health():
    return JSONResponse(content={"status": "healthy"}, status_code=200)

@app.post("/remove-bg")
async def remove_bg(image: UploadFile = File(...)):
    try:
        # Open the uploaded image
        input_img = Image.open(image.file)

        # Remove background
        output_img = remove(input_img)

        # Save the output image to a buffer
        buf = io.BytesIO()
        output_img.save(buf, format="PNG")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
