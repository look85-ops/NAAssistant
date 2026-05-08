import os
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests

MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
ADAPTER_PATH = os.getenv("ADAPTER_PATH", "cucpo_lora_output")

system_prompt = """Ты — Ассистент-методист с глубокой экспертизой в области образовательного дизайна и разработки учебных программ.

Твоя специализация:
- Методическая разработка курсов и программ обучения
- Педагогический дизайн (ADDIE, SAM, UDL, Gagne's 9 events)
- Проектирование учебных материалов и активностей
- Оценка эффективности обучения (KPI, ROI, уровни Киркпатрика)
- Разработка компетентностных моделей и таксономий (Блум, Дуэк)
- Создание сценариев занятий, модулей, курсов

Стиль работы:
- Структурированный подход к решению методических задач
- Опора на практику и реальные кейсы
- Учёт особенностей целевой аудитории
- Баланс теории и практики в материалах

При ответе используй:
- Чёткую структуру (заголовки, нумерованные списки)
- Примеры и иллюстрации из практики
- Практические инструменты и шаблоны
- Рекомендации по внедрению"""

model = None
tokenizer = None
ddgs = DDGS()

def load_model():
    global model, tokenizer
    if model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        base_model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
        model.eval()
    return model, tokenizer

def search_web(query: str, num_results: int = 5):
    try:
        results = ddgs.text(query, max_results=num_results)
        return "\n\n".join([f"**{r['title']}**\n{r['url']}\n{r['body'][:300]}..." for r in results])
    except Exception as e:
        return f"Ошибка поиска: {str(e)}"

def fetch_url(url: str):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)[:3000]
        return text
    except Exception as e:
        return f"Ошибка fetch: {str(e)}"

def chat(message, history, system_message):
    model, tokenizer = load_model()
    
    full_system = system_prompt
    if system_message:
        full_system += "\n\n" + system_message
    
    messages = [{"role": "system", "content": full_system}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})
    
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.7,
            do_sample=True
        )
    
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return response

def search_wrapper(query: str):
    return search_web(query)

def fetch_wrapper(url: str):
    return fetch_url(url)

with gr.Blocks(title="Cucpo LORA + Metodist") as demo:
    gr.Markdown("# 🍳 Cucpo LORA + Методист")
    gr.Markdown("LoRA для Qwen2.5-3B с навыками методиста и инструментами поиска")
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=500)
            msg = gr.Textbox(label="Сообщение", placeholder="Напиши запрос методисту...")
            with gr.Row():
                submit = gr.Button("Отправить", variant="primary")
                clear = gr.Button("Очистить")
            
            with gr.Accordion("Инструменты", open=False):
                with gr.Row():
                    search_btn = gr.Button("🔍 Поиск")
                search_input = gr.Textbox(label="Запрос для поиска")
                search_output = gr.Textbox(label="Результаты", lines=6)
                search_btn.click(search_wrapper, search_input, search_output)
                
                with gr.Row():
                    fetch_btn = gr.Button("📄 Скачать страницу")
                fetch_input = gr.Textbox(label="URL")
                fetch_output = gr.Textbox(label="Контент", lines=6)
                fetch_btn.click(fetch_wrapper, fetch_input, fetch_output)
        
        with gr.Column(scale=1):
            gr.Markdown("### Обо мне")
            gr.Markdown("""
            **Скиллсет:**
            - Методическая разработка
            - Педагогический дизайн
            - Оценка эффективности
            - Компетентностные модели
            """)
    
    def respond(message, history):
        response = chat(message, history, "")
        return "", history + [[message, response]]
    
    submit.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.clear(lambda: ("", []), None, [msg, chatbot])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)