from fastapi import FastAPI, Request
import requests
from io import BytesIO
from PIL import Image
import base64

app = FastAPI()

@app.post("/api/process-image")
async def process_image(request: Request):
    body = await request.json()
    image_url = body["url"]

    # Download image
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Resize and convert to RGB JPEG
    image = image.convert("RGB")
    image = image.resize((128, 128))  # Example size

    # Convert to raw pixel data
    pixels = list(image.getdata())
    flat_pixels = [val for rgb in pixels for val in rgb]  # Flatten RGB

    # Convert to base64 for transmission
    byte_data = bytes(flat_pixels)
    encoded = base64.b64encode(byte_data).decode("utf-8")

    return { "pixelData": encoded, "width": 128, "height": 128 }
