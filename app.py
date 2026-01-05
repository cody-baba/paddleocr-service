from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
from PIL import Image
import io

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

@app.post("/ocr")
async def ocr_endpoint(request: Request):
    try:
        form = await request.form()
        upload = form.get("file")

        if not upload:
            return JSONResponse(status_code=400, content={"error": "Missing file field 'file'"})

        image_bytes = await upload.read()
        print(f"Received file: {upload.filename}, size: {len(image_bytes)} bytes")

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"Invalid image: {str(e)}"})

        try:
            result = ocr.ocr(image, cls=True)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"OCR failed: {str(e)}"})

        return {
            "filename": upload.filename,
            "count": len(result[0]),
            "items": result[0]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Unhandled server error: {str(e)}"})
