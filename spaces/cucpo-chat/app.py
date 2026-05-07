import os
from typing import List, Tuple

import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

try:
    from huggingface_hub import snapshot_download
except Exception:
    snapshot_download = None


# Lazy singletons
_model = None
_tokenizer = None


def _read_if_exists(path: str) -> str:
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""


def load_model():
    global _model, _tokenizer
    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    base_model_id = os.getenv("BASE_MODEL_ID", "unsloth/DeepSeek-R1-Distill-Qwen-7B-bnb-4bit")

    # Where to get LoRA adapters from:
    # 1) LORA_PATH -> local dir with adapter_model.safetensors
    # 2) LORA_REPO_ID -> HF repo id (will be downloaded to ./cucpo_lora)
    lora_path = os.getenv("LORA_PATH", os.path.join(os.path.dirname(__file__), "cucpo_lora"))
    # Fallback to expected public repo under your account; update if needed
    lora_repo_id = os.getenv("LORA_REPO_ID", "Thrgbbnh/cucpo_lora")

    adapter_dir = None
    if os.path.isdir(lora_path) and os.path.isfile(os.path.join(lora_path, "adapter_model.safetensors")):
        adapter_dir = lora_path
    elif lora_repo_id:
        if snapshot_download is None:
            raise RuntimeError("huggingface_hub not available to download LORA_REPO_ID")
        local_dir = os.path.join(os.path.dirname(__file__), "cucpo_lora")
        os.makedirs(local_dir, exist_ok=True)
        adapter_dir = snapshot_download(repo_id=lora_repo_id, local_dir=local_dir)
    else:
        raise FileNotFoundError(
            "LoRA adapters not found. Provide LORA_PATH (local) or LORA_REPO_ID (HuggingFace)."
        )

    # Prefer GPU; on CPU avoid half-precision to prevent unsupported dtype errors
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    # Load base model (bnb-4bit quantized in base repo)
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_fast=True, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )

    # Attach LoRA
    model = PeftModel.from_pretrained(model, adapter_dir)

    # Apply optional chat template shipped with LoRA
    chat_template_path = os.path.join(adapter_dir, "chat_template.jinja")
    chat_template = _read_if_exists(chat_template_path)
    if chat_template:
        tokenizer.chat_template = chat_template

    _model, _tokenizer = model, tokenizer
    return _model, _tokenizer


def _messages_from_history(history: List[Tuple[str, str]], system_prompt: str, user_message: str):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for user, assistant in history:
        if user:
            messages.append({"role": "user", "content": user})
        if assistant:
            messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": user_message})
    return messages


def generate_reply(user_message: str, history: List[Tuple[str, str]], system_prompt: str,
                   max_new_tokens: int = 1024, temperature: float = 0.5, top_p: float = 0.9) -> str:
    model, tokenizer = load_model()
    messages = _messages_from_history(history, system_prompt, user_message)

    # Use chat template if available
    if getattr(tokenizer, "chat_template", None):
        input_ids = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt",
        )
    else:
        # Fallback: simple formatting
        prompt = "".join(
            [f"User: {m['content']}\n" if m["role"] == "user" else (f"System: {m['content']}\n" if m["role"] == "system" else f"Assistant: {m['content']}\n") for m in messages]
        ) + "Assistant:"
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    input_ids = input_ids.to(model.device if hasattr(model, "device") else (0 if torch.cuda.is_available() else "cpu"))
    with torch.no_grad():
        output_ids = model.generate(
            input_ids=input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=1.05,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Only decode the generated continuation
    gen_ids = output_ids[0, input_ids.shape[-1]:]
    text = tokenizer.decode(gen_ids, skip_special_tokens=True)
    return text.strip()


def chat_fn(message: str, history: List[Tuple[str, str]], system_prompt: str,
            max_new_tokens: int, temperature: float, top_p: float) -> str:
    return generate_reply(message, history, system_prompt, max_new_tokens, temperature, top_p)


demo = gr.ChatInterface(
    fn=chat_fn,
    additional_inputs=[
        gr.Textbox(label="Системное сообщение", value="Ты аккуратный ассистент. Отвечай кратко и по делу.", lines=2),
        gr.Slider(64, 2048, value=1024, step=16, label="Макс. токенов ответа"),
        gr.Slider(0.0, 1.5, value=0.5, step=0.05, label="Temperature"),
        gr.Slider(0.1, 1.0, value=0.9, step=0.05, label="top_p"),
    ],
    title="CUCPO LoRA Chat",
    description=(
        "Чат-демо на базе DeepSeek-R1-Distill-Qwen-7B (4-bit) с LoRA-адаптером.\n"
        "Если Space на CPU, ответы могут генерироваться очень медленно."
    ),
)

if __name__ == "__main__":
    # For local testing: python app.py
    load_model()  # warmup load to fail fast if misconfigured
    demo.queue().launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", "7860")))
