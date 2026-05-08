import os
import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

try:
    from huggingface_hub import snapshot_download
except Exception:
    snapshot_download = None

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
    lora_path = os.getenv("LORA_PATH", os.path.join(os.path.dirname(__file__), "cucpo_lora"))
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
        raise FileNotFoundError("Provide LORA_PATH or LORA_REPO_ID for adapters")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    tokenizer = AutoTokenizer.from_pretrained(base_model_id, use_fast=True, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=dtype,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    model = PeftModel.from_pretrained(model, adapter_dir)

    chat_template_path = os.path.join(adapter_dir, "chat_template.jinja")
    chat_template = _read_if_exists(chat_template_path)
    if chat_template:
        tokenizer.chat_template = chat_template

    _model, _tokenizer = model, tokenizer
    return _model, _tokenizer


def generate_reply(user_message: str, history, system_prompt: str, max_new_tokens: int, temperature: float, top_p: float) -> str:
    model, tokenizer = load_model()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for u, a in history:
        if u:
            messages.append({"role": "user", "content": u})
        if a:
            messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": user_message})

    if getattr(tokenizer, "chat_template", None):
        input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
    else:
        prompt = "".join([
            (f"System: {m['content']}\n" if m["role"] == "system" else (f"User: {m['content']}\n" if m["role"] == "user" else f"Assistant: {m['content']}\n"))
            for m in messages
        ]) + "Assistant:"
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
    gen_ids = output_ids[0, input_ids.shape[-1]:]
    text = tokenizer.decode(gen_ids, skip_special_tokens=True)
    return text.strip()


def main():
    st.set_page_config(page_title="CUCPO LoRA Chat", layout="wide")
    st.title("CUCPO LoRA Chat")
    st.caption("Если Space запущен на CPU, модель не загрузится — включите Community GPU в Settings → Hardware.")

    # Block early on CPU to avoid runtime errors with 7B 4-bit base
    if not torch.cuda.is_available():
        st.error(
            "Для запуска этой модели нужен GPU. Открой Settings → Hardware и выбери Community GPU (бесплатно) или T4.")
        st.info("После переключения подождите пересборку и обновите страницу.")
        return

    with st.sidebar:
        system_prompt = st.text_area("Системное сообщение", value="Ты аккуратный ассистент. Отвечай кратко и по делу.", height=80)
        max_new_tokens = st.slider("Макс. токенов ответа", 64, 2048, 1024, step=16)
        temperature = st.slider("Temperature", 0.0, 1.5, 0.5, step=0.05)
        top_p = st.slider("top_p", 0.1, 1.0, 0.9, step=0.05)
        if st.button("Загрузить/прогреть модель"):
            load_model()
            st.success("Модель загружена")

    if "history" not in st.session_state:
        st.session_state.history = []

    for u, a in st.session_state.history:
        with st.chat_message("user"):
            st.write(u)
        if a:
            with st.chat_message("assistant"):
                st.write(a)

    user_message = st.chat_input("Напиши вопрос…")
    if user_message:
        st.session_state.history.append((user_message, None))
        with st.chat_message("user"):
            st.write(user_message)
        with st.chat_message("assistant"):
            with st.spinner("Генерация ответа…"):
                reply = generate_reply(user_message, st.session_state.history[:-1], system_prompt, max_new_tokens, temperature, top_p)
                st.write(reply)
        st.session_state.history[-1] = (user_message, reply)


if __name__ == "__main__":
    main()
