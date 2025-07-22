from fastapi import FastAPI, Request
from PIL import Image
from io import BytesIO
import requests
import base64
import uvicorn

app = FastAPI()

@app.post("/process")
async def process_images(request: Request):
    data = await request.json()
    results = []

    for post in data[:10]:  # limitar a 10 para testes
        file_url = post.get("file", {}).get("url")
        if not file_url:
            continue
        try:
            img_response = requests.get(file_url, timeout=5)
            img = Image.open(BytesIO(img_response.content)).convert("RGB")
            img = img.resize((128, 128))

            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=70)
            encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

            results.append(encoded)
        except:
            continue

    return {"images": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
