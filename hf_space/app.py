import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

OPENROUTER_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.getenv("BOT_MODEL", "deepseek/deepseek-chat")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "bot-mvp"}


@app.post("/chat")
async def chat(request: Request):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return JSONResponse({"error": "OPENROUTER_API_KEY is not set"}, status_code=500)
    try:
        data = await request.json()
    except Exception:
        data = {}

    message = data.get("message")
    messages = data.get("messages")
    model = data.get("model", DEFAULT_MODEL)
    if messages is None:
        if not message:
            return JSONResponse({"error": "Provide 'message' or 'messages'"}, status_code=400)
        messages = [{"role": "user", "content": str(message)}]

    payload = {"model": model, "messages": messages}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = f"{OPENROUTER_URL}/chat/completions"

    timeout = httpx.Timeout(45.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=payload, headers=headers)
        if resp.status_code >= 400:
            return JSONResponse({"error": "upstream_error", "status": resp.status_code, "body": resp.text}, status_code=502)
        data = resp.json()
        out = None
        try:
            out = data["choices"][0]["message"]["content"]
        except Exception:
            pass
        return {"model": model, "output": out, "raw": data}
