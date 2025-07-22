from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import aiohttp
import io
import base64

app = FastAPI()

class ImageRequest(BaseModel):
    url: str
    width: int = 128
    height: int = 128

@app.post("/process-image")
async def process_image(req: ImageRequest):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(req.url) as resp:
                if resp.status != 200:
                    return {"error": "Failed to download image"}
                data = await resp.read()
    except Exception as e:
        return {"error": str(e)}

    try:
        image = Image.open(io.BytesIO(data)).convert("RGB")
        image = image.resize((req.width, req.height), Image.LANCZOS)

        raw_bytes = image.tobytes()
        encoded = base64.b64encode(raw_bytes).decode("ascii")

        return {
            "width": req.width,
            "height": req.height,
            "pixels": encoded
        }

    except Exception as e:
        return {"error": str(e)}
