from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Libera requisições de qualquer origem (para Roblox)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def root(request: Request):
    body = await request.json()
    tags = body.get("tags", "")
    page = body.get("page", 1)

    response = requests.get(
        "https://e621.net/posts.json",
        params={"tags": tags, "page": page, "limit": 10},
        headers={"User-Agent": "e621byrogerinho/1.0 userscript"}
    )

    if response.status_code != 200:
        return {"error": "Erro ao buscar"}

    data = response.json()
    posts = data.get("posts", [])
    images = []

    for post in posts:
        if "file" in post and "url" in post["file"]:
            images.append(post["file"]["url"])

    return {"images": images}
