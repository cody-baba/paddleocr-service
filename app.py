from fastapi import FastAPI, UploadFile, File
from paddleocr import PaddleOCR
from PIL import Image
import io

app = FastAPI()
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 'ch' for Simplified Chinese, use 'chinese_cht' for Traditional

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    img = Image.open(io.BytesIO(content)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    result = ocr.ocr(buf.getvalue(), cls=True)

    items = []
    for page in result:
        for line in page:
            box, (text, prob) = line
            items.append({
                "text": text,
                "confidence": float(prob),
                "box": box
            })
    return {"count": len(items), "items": items}
