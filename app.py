from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io

# Import PaddleOCR
from paddleocr import PaddleOCR

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # adjust lang if needed

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    try:
        # Read file bytes
        image_bytes = await file.read()
        if not image_bytes:
            return JSONResponse(status_code=400, content={"error": "No file content received"})

        print(f"Received file: {file.filename}, size: {len(image_bytes)} bytes")

        # Try to open image
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"Invalid image: {str(e)}"})

        # Run OCR
        result = ocr.ocr(image, cls=True)

        return {
            "filename": file.filename,
            "count": len(result[0]),
            "items": result[0]
        }

    except Exception as e:
        print(f"Server error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
