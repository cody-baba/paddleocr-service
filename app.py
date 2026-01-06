from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
from PIL import Image
import io

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ocr")
async def ocr_endpoint(request: Request):
    try:
        form = await request.form()
        upload = form.get("file")

        if not upload:
            return JSONResponse(status_code=400, content={"error": "Missing file field 'file'"})

        # Case 1: n8n sends a file-like object
        if hasattr(upload, "read"):
            image_bytes = await upload.read()
            filename = getattr(upload, "filename", "unknown")
        # Case 2: n8n sends a string (path or base64)
        elif isinstance(upload, str):
            return JSONResponse(
                status_code=400,
                content={"error": f"Received string instead of file: {upload}"}
            )
        else:
            return JSONResponse(status_code=400, content={"error": "Unsupported upload type"})

        print(f"Received file: {filename}, size: {len(image_bytes)} bytes")

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"Invalid image: {str(e)}"})

        try:
            result = ocr.ocr(image)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"OCR failed: {str(e)}"})

        return {
            "filename": filename,
            "count": len(result[0]),
            "items": result[0]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unhandled server error: {str(e)}"})
