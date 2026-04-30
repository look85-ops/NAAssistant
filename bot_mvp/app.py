import os
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)


OPENROUTER_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.getenv("BOT_MODEL", "deepseek/deepseek-chat")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/chat")
def chat():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return jsonify({"error": "OPENROUTER_API_KEY is not set"}), 500

    try:
        data = request.get_json(force=True, silent=True) or {}
    except Exception:
        data = {}

    # Accept either a single 'message' or a full 'messages' array
    message = data.get("message")
    messages = data.get("messages")
    model = data.get("model", DEFAULT_MODEL)

    if messages is None:
        if not message:
            return jsonify({"error": "Provide 'message' (string) or 'messages' (array)"}), 400
        messages = [{"role": "user", "content": str(message)}]

    payload = {
        "model": model,
        "messages": messages,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            f"{OPENROUTER_URL}/chat/completions",
            json=payload,
            headers=headers,
            timeout=45,
        )
        if resp.status_code >= 400:
            return jsonify({"error": "upstream_error", "status": resp.status_code, "body": resp.text}), 502
        out = resp.json()
        text = None
        try:
            text = out["choices"][0]["message"]["content"]
        except Exception:
            pass
        return jsonify({"model": model, "output": text, "raw": out})
    except requests.Timeout:
        return jsonify({"error": "upstream_timeout"}), 504
    except Exception as e:
        return jsonify({"error": "internal_error", "detail": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
