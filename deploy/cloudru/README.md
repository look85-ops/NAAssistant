Деплой CUCPO-чат в Cloud.ru (GPU VM)

Требования
- Учётная запись Cloud.ru и доступ к Evolution Compute (ВМ)
- ВМ с GPU (например, NVIDIA T4 16GB), 4+ vCPU, 16–32GB RAM, диск 50–100GB
- Открытые порты 80/443 (для 443 нужен домен и сертификат; базово хватит 80)

Шаги
1. Создать ВМ c Ubuntu 22.04+, подключить публичный IP.
2. Установить Docker и Docker Compose:
   sudo apt-get update -y && sudo apt-get install -y ca-certificates curl gnupg
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update -y && sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   sudo usermod -aG docker $USER && newgrp docker

3. Скопировать файлы деплоя на сервер:
   - Папка deploy/cloudru: docker-compose.yml и .env.example
   Заполните .env на основе .env.example:
   cp .env.example .env
   # при необходимости добавьте HF_TOKEN=hf_xxx

4. Сборка и запуск:
   docker compose build
   docker compose up -d

5. Проверка:
   - Откройте http://<публичный_IP>/ в браузере.
   - Первый запуск может быть долгим (скачивание модели/LoRA).

Заметки
- Для HTTPS добавьте реверс-прокси (Nginx/Caddy) перед приложением и выпустите сертификат Let’s Encrypt.
- Если GPU недоступен в регионе/тарифе, можно стартовать на CPU, но 7B 4-bit будет работать медленно. Рассмотрите меньшую базу (1.5–3B) — потребуется правка BASE_MODEL_ID в .env.
