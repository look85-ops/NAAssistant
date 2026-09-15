"""Скрипт логина в hh.ru — отдельный профиль для мониторинга."""
import time
from playwright.sync_api import sync_playwright

# Отдельный профиль — не конфликтует с MCP-браузером
PROFILE = r"C:\Users\marcenuk\Desktop\Новый проект\scripts\browser-state\hh-profile-monitor"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        PROFILE, headless=False, viewport={"width": 1280, "height": 800}
    )
    page = ctx.new_page()
    page.goto("https://hh.ru/account/login?role=applicant&backurl=%2F&hhtmFrom=main", timeout=60000)
    page.wait_for_load_state("domcontentloaded")
    print("Окно браузера открыто. Введи логин и пароль.")
    print("Скрипт ждёт, когда ты попадёшь на главную hh.ru...")
    for i in range(240):
        time.sleep(1)
        url = page.url
        if "hh.ru" in url and "/login" not in url and "/account" not in url:
            print(f"Вход выполнен! Профиль сохранён: {PROFILE}")
            break
        if i % 30 == 29:
            print(f"  ...жду ({int((i+1)*1)} сек), URL: {url[:90]}")
    else:
        print("Таймаут. Закрой окно и попробуй снова.")
    ctx.close()
    print("Окно закрыто.")