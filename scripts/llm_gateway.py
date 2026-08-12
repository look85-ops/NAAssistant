#!/usr/bin/env python3
"""llm_gateway.py — единая точка вызова LLM для агентов NM.ASSISTANT.

Что делает:
- Провайдеры: OpenRouter, DeepSeek, Gemini и любой OpenAI-совместимый
  прокси (PROXY_URL / BOTHUB_URL). Ключи из env или файлов API.txt /
  DGAPIFREE.txt рядом с вызывающим скриптом.
- retry + fallback: пробует провайдеров по очереди, пока не получит текст.
- call_json: вызывает, вытаскивает JSON из ответа, валидирует по схеме,
  при ошибке парсинга/валидации переспрашивает модель один раз с текстом
  ошибки.
- extract_json: устойчивое извлечение JSON (код-фенсы, мусор вокруг).
- Валидация без pydantic: типы, обязательные поля, допустимые значения.
- Лог токенов/затрат в llm_usage.log (рядом с вызвавшим скриптом).

Зависимости: только requests. Python 3.8+.
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PROXY_URL = "https://openai.bothub.chat/v1"


# ─── настройка провайдеров ─────────────────────────────────────────

class Provider:
    def __init__(self, name, api_key, base_url, models, kind="openai", free=False):
        self.name = name
        self.api_key = api_key
        self.base_url = base_url
        self.models = models
        self.kind = kind          # "openai" | "gemini"
        self.free = free

    def __repr__(self):
        return f"<Provider {self.name} free={self.free}>"


def _read_env_or_file(name, *paths):
    """Значение из env, иначе первая непустая строка из файлов."""
    val = os.environ.get(name, "").strip()
    if val:
        return val
    for p in paths:
        p = Path(p)
        if p.exists():
            try:
                raw = p.read_text(encoding="utf-8", errors="ignore").strip()
            except OSError:
                continue
            if raw:
                return raw
    return ""


def _read_key_value_file(text):
    """Разбирает формат 'model:key' по строкам. Пустые строки игнорирует."""
    out = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        model, key = line.split(":", 1)
        model, key = model.strip(), key.strip()
        if model and key:
            out.append((model, key))
    return out


def _norm_base(base):
    if base.endswith("/chat/completions"):
        return base
    return base.rstrip("/") + "/chat/completions"


class LLMGateway:
    """Очередь провайдеров с retry/fallback и валидацией ответов."""

    def __init__(self, base_dir=None):
        self.providers = []
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.log_path = self.base_dir / "llm_usage.log"

    # ── регистрация ──────────────────────────────────────────────

    def add_openai_provider(self, name, api_key, base_url, models=None, free=False):
        if api_key:
            self.providers.append(Provider(
                name, api_key, _norm_base(base_url), models or ["gpt-3.5-turbo"],
                kind="openai", free=free))
            return True
        return False

    def add_gemini_provider(self, api_key, model=None):
        if api_key:
            model = model or os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
            self.providers.append(Provider(
                "gemini", api_key, "", [model], kind="gemini"))
            return True
        return False

    def auto_configure(self, base_dir=None, proxy_url=None):
        """Читает env и файлы ключей в base_dir и регистрирует провайдеров.

        Порядок приоритета (первый в списке — первый в fallback-цепи):
        1. OpenRouter (OPENROUTER_API_KEY)
        2. NVIDIA NIM (NVIDIA_API_KEY, OpenAI-совместимый)
        3. DeepSeek (DEEPSEEK_API_KEY)
        4. Gemini (GEMINI_API_KEY)
        5. API.txt 'model:key' -> PROXY_URL / BOTHUB_URL / дефолт
        6. DGAPIFREE.txt / FREE_API_KEYS (deepseek free)
        """
        if base_dir:
            self.base_dir = Path(base_dir)
            self.log_path = self.base_dir / "llm_usage.log"

        # 1. OpenRouter
        key = os.environ.get("OPENROUTER_API_KEY", "")
        if key:
            model = os.environ.get("OPENROUTER_MODEL", "qwen/qwen3-coder:free")
            self.add_openai_provider("openrouter", key,
                                     "https://openrouter.ai/api/v1", [model],
                                     free=":free" in model)

        # 2. NVIDIA NIM (доступен из РФ; Kimi K2.x)
        key = os.environ.get("NVIDIA_API_KEY", "")
        if key:
            model = os.environ.get("NVIDIA_MODEL", "moonshotai/kimi-k2.6")
            self.add_openai_provider("nvidia", key,
                                     "https://integrate.api.nvidia.com/v1", [model])

        # 3. DeepSeek
        key = os.environ.get("DEEPSEEK_API_KEY", "")
        if key:
            self.add_openai_provider("deepseek", key,
                                     "https://api.deepseek.com/v1", ["deepseek-chat"])

        # 4. Gemini
        self.add_gemini_provider(os.environ.get("GEMINI_API_KEY", ""))

        # 5. API.txt (model:key) -> OpenAI-совместимый прокси
        raw = _read_env_or_file("EITHER_API_KEY", self.base_dir / "API.txt")
        base = proxy_url or os.environ.get("PROXY_URL", "") or \
            os.environ.get("BOTHUB_URL", DEFAULT_PROXY_URL)
        base = base.replace("/chat/completions", "").rstrip("/")
        for model, key in _read_key_value_file(raw):
            self.add_openai_provider(f"proxy-{model}", key,
                                     base + "/chat/completions", [model],
                                     free=False)

        # 6. DeepSeek free-ключи (DGAPIFREE.txt / FREE_API_KEYS)
        raw_free = _read_env_or_file("FREE_API_KEYS", self.base_dir / "DGAPIFREE.txt")
        for line in raw_free.strip().splitlines():
            line = line.strip()
            if not line.startswith("sk-"):
                continue
            self.add_openai_provider(f"deepseek-free-{line[-8:]}", line,
                                     "https://api.deepseek.com/v1/chat/completions",
                                     ["deepseek-chat"], free=True)

        return self.providers

    # ── вызов ────────────────────────────────────────────────────

    def _payload_openai(self, model, prompt, temperature, max_tokens):
        return {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

    def _payload_gemini(self, model, prompt, temperature, max_tokens):
        return {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

    def _request(self, provider, model, prompt, temperature, max_tokens, timeout):
        headers = {"Content-Type": "application/json"}
        if provider.kind == "gemini":
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{model}:generateContent?key={provider.api_key}")
        else:
            headers["Authorization"] = f"Bearer {provider.api_key}"
            url = provider.base_url
        payload = (self._payload_gemini(model, prompt, temperature, max_tokens)
                   if provider.kind == "gemini"
                   else self._payload_openai(model, prompt, temperature, max_tokens))
        resp = requests_post(url, headers=headers, json=payload, timeout=timeout)
        return resp

    def call(self, prompt, *, model=None, temperature=0.7, max_tokens=2000,
             prefer_free=False, timeout=120, max_attempts=2):
        """Возвращает текст ответа или None, если все провайдеры не ответили."""
        providers = list(self.providers)
        if prefer_free:
            providers.sort(key=lambda p: (not p.free, p.name))
        if model:
            # Сначала провайдеры, у которых есть запрошенная модель;
            # остальные — запасные (возьмут свою модель).
            providers = ([p for p in providers if model in p.models] +
                         [p for p in providers if model not in p.models])

        if not providers:
            return None

        for _attempt in range(max(1, max_attempts)):
            for provider in providers:
                if model and model in provider.models:
                    targets = [model]
                else:
                    targets = provider.models
                for mdl in targets:
                    try:
                        resp = self._request(provider, mdl, prompt,
                                             temperature, max_tokens, timeout)
                        if resp.status_code >= 400:
                            self._log("error", provider.name, mdl, "", 0,
                                      f"HTTP {resp.status_code}: {resp.text[:120]}")
                            continue
                        data = resp.json()
                        text, in_tok, out_tok = self._parse(provider, data)
                        if text and len(text.strip()) > 0:
                            self._log("ok", provider.name, mdl, text,
                                      in_tok + out_tok, "")
                            return text
                        self._log("error", provider.name, mdl, "", 0, "пустой ответ")
                    except Exception as e:
                        self._log("error", provider.name, mdl, "", 0, str(e)[:120])
                        continue
        return None

    def _parse(self, provider, data):
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(str(data["error"]))
        in_tok = out_tok = 0
        if provider.kind == "gemini":
            cands = data.get("candidates", [])
            text = ""
            if cands:
                parts = cands[0].get("content", {}).get("parts", [])
                text = parts[0].get("text", "") if parts else ""
            usage = data.get("usageMetadata", {})
            in_tok = usage.get("promptTokenCount", 0)
            out_tok = usage.get("candidatesTokenCount", 0)
            return text, in_tok, out_tok
        usage = data.get("usage", {})
        in_tok = usage.get("prompt_tokens", 0)
        out_tok = usage.get("completion_tokens", 0)
        msg = data.get("choices", [{}])[0].get("message", {})
        return (msg.get("content", "") or msg.get("reasoning", ""), in_tok, out_tok)

    def call_json(self, prompt, *, schema=None, item_schema=None, **kwargs):
        """call() + извлечение JSON + валидация. Один повтор с текстом ошибки."""
        text = self.call(prompt, **kwargs)
        if text is None:
            return None
        data = extract_json(text)
        if data is not None and schema:
            err = validate(data, schema, item_schema)
            if err:
                data = None
        if data is not None:
            return data
        # Повтор: просим модель вернуть корректный JSON
        fix_prompt = (
            f"{prompt}\n\nВ прошлый раз ответ был невалидным JSON "
            f"(или не прошёл проверку). Верни ТОЛЬКО корректный JSON "
            f"строго в требуемом формате, без markdown-обёртки."
        )
        text2 = self.call(fix_prompt, **kwargs)
        if text2 is None:
            return None
        data2 = extract_json(text2)
        if data2 is not None and schema:
            err = validate(data2, schema, item_schema)
            if err:
                return None
        return data2

    def _log(self, status, provider, model, text, tokens, note):
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                entry = {
                    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    "status": status,
                    "provider": provider,
                    "model": model,
                    "tokens": tokens,
                    "note": note[:200],
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass


# ─── модульные помощники ──────────────────────────────────────────

def requests_post(*args, **kwargs):
    import requests
    return requests.post(*args, **kwargs)


def extract_json(text):
    """Вытаскивает первый валидный JSON-объект/массив из текста.

    Обрабатывает: markdown-фенсы, мусор вокруг, несколько JSON-фрагментов.
    """
    if not text:
        return None
    text = re.sub(r"```(?:json)?\s*", "", text).replace("```", "").strip()
    start = text.find("{")
    if start == -1:
        start = text.find("[")
        if start == -1:
            return None
        return _scan_json(text, start, "[", "]")
    return _scan_json(text, start, "{", "}")


def _scan_json(text, start, open_ch, close_ch):
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def validate(data, schema, item_schema=None):
    """Проверяет data по схеме {поле: (тип, обязательное, допустимые)}.

    item_schema применяется к элементам списков. Возвращает строку ошибки
    или None, если всё ок.
    """
    if not isinstance(data, dict):
        return f"ожидался объект, получено {type(data).__name__}"
    for field, (ftype, required, allowed) in schema.items():
        if field not in data:
            if required:
                return f"нет поля '{field}'"
            continue
        val = data[field]
        if ftype == "str" and not isinstance(val, str):
            return f"поле '{field}': ожидалась строка, получено {type(val).__name__}"
        if ftype == "int" and not isinstance(val, int):
            return f"поле '{field}': ожидалось число"
        if ftype == "list":
            if not isinstance(val, list):
                return f"поле '{field}': ожидался список"
            if item_schema:
                for i, item in enumerate(val):
                    err = validate(item, item_schema)
                    if err:
                        return f"поле '{field}[{i}]': {err}"
        if allowed and val not in allowed:
            return f"поле '{field}': недопустимое значение '{val}'"
    return None
