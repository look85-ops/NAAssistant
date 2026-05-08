---
title: CUCPO Chat
emoji: 🗣️
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 4.31.0
python_version: "3.10"
app_file: app.py
pinned: false
---

CUCPO LoRA Chat — Hugging Face Space

Как запустить локально
1. Установите зависимости: pip install -r requirements.txt
2. Положите папку с адаптером LoRA (adapter_model.safetensors и adapter_config.json) в spaces/cucpo-chat/cucpo_lora или укажите путь через переменную окружения LORA_PATH.
3. Укажите базовую модель (по умолчанию unsloth/DeepSeek-R1-Distill-Qwen-7B-bnb-4bit) через BASE_MODEL_ID при необходимости.
4. Старт: python app.py

Деплой в Hugging Face Spaces
- Создайте Space (Gradio) и загрузите содержимое папки spaces/cucpo-chat.
- В Settings -> Variables можно задать:
  - LORA_REPO_ID: repo с адаптером (например, username/cucpo-lora)
  - BASE_MODEL_ID: базовая модель (по умолчанию unsloth/DeepSeek-R1-Distill-Qwen-7B-bnb-4bit)
  - HF_TOKEN: если требуется приватный доступ
- Тип железа: рекомендуется T4 small/medium, A10G — быстрее.
 - Если Space на CPU: модель 7B в 4-bit будет работать крайне медленно или не запустится. Рассмотрите меньшую базовую модель (1.5B–3B) или Community GPU.

Загрузка адаптера
- Приоритет LORA_PATH (локальная папка) > LORA_REPO_ID (скачивание из HF).
- Если есть chat_template.jinja в папке адаптера, он будет применён.

Приватный/публичный доступ
- Space можно сделать Private и поделиться ссылкой/добавить коллабораторов.
- Для публичного доступа включите Public в настройках Space.

Примечания
- Модель 7B в 4-bit обычно умещается в T4 16GB. При CPU-типе работать будет очень медленно.
