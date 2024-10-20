from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server is running."}

@app.get("/health")
def health():
    return JSONResponse(content={"status": "healthy"}, status_code=200)
