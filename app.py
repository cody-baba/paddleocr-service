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

        image_bytes = await upload.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        result = ocr.ocr(image, cls=True)

        return {
            "filename": upload.filename,
            "count": len(result[0]),
            "items": result[0]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
