"""Запускает headed Chromium, ждёт пока Наташа войдёт в hh.ru, сохраняет сессию."""
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\marcenuk\Desktop\Новый проект\scripts\browser-state\hh-profile"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False,
        viewport={"width": 1280, "height": 800},
    )
    page = context.new_page()

    page.goto("https://hh.ru/account/login?role=applicant&backurl=%2F&hhtmFrom=main", timeout=60000)
    page.wait_for_load_state("domcontentloaded")

    print("Окно браузера открыто. Введи логин и пароль.")
    print("(скрипт ждёт, когда ты попадёшь на главную hh.ru без /login)")

    logged_in = False
    for i in range(180):
        time.sleep(1)
        url = page.url
        if "hh.ru" in url and "/login" not in url and "/account" not in url:
            logged_in = True
            break
        if i % 15 == 14:
            print(f"  ...жду входа ({i+1} сек), текущий URL: {url[:80]}")

    if logged_in:
        print("Вход подтверждён! Сессия сохранена в профиле Chromium.")
        print(f"Профиль: {USER_DATA_DIR}")
        print("Теперь перезапусти opencode — браузер будет залогинен.")
    else:
        print("Таймаут. Закрой окно и запусти скрипт снова.")

    context.close()
    print("Окно браузера закрыто.")