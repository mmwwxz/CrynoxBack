# https://crynox.tech/

**Start Deploy:**

1. `git clone 'repo'`: Клонирует репозиторий.
2. `cd 'repo'`: Переходит в каталог репозитория.
3. `sudo apt update && sudo apt upgrade -y`: Обновляет и обновляет все пакеты в системе.
4. `sudo apt install ca-certificates curl gnupg lsb-release unzip`: Устанавливает необходимые пакеты и утилиты.
5. `sudo mkdir -p /etc/apt/keyrings`: Создает каталог для ключей APT.
6. `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`: Устанавливает GPG ключ для Docker.
7. `echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`: Добавляет официальный репозиторий Docker в список APT.
8. `sudo apt update`: Обновляет список пакетов после добавления репозитория Docker.
9. `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`: Устанавливает Docker и его компоненты.
10. `sudo usermod -aG docker $USER`: Добавляет текущего пользователя в группу Docker.
11. `id $USER`: Отображает идентификаторы пользователя.
12. `newgrp docker`: Перезапускает оболочку для применения изменений в группах.
13. `sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`: Загружает Docker Compose.
14. `sudo chmod +x /usr/local/bin/docker-compose`: Добавляет права на выполнение для Docker Compose.
15. `docker run hello-world`: Запускает контейнер Hello World для проверки Docker.
16. `docker-compose --version`: Проверяет версию Docker Compose.
17. `docker-compose up --build -d`: Запускает контейнеры из docker-compose.yml в фоновом режиме.
18. `docker-compose exec web python manage.py collectstatic --no-input`: Собирает статические файлы Django.
19. `docker-compose exec web python manage.py createsuperuser`: Создает суперпользователя Django.
20. `sudo docker-compose ps -a`: Показывает статус всех контейнеров Docker Compose.
21. `sudo docker-compose logs`: Показывает логи Docker Compose.
22. `sudo lsof -i :80`: Показывает процессы, слушающие порт 80.


**Ssl certbot:**

1. `sudo apt update`: Обновление списка пакетов.

2. `sudo apt install nginx`: Установка веб-сервера Nginx.

3. `sudo apt install certbot python3-certbot-nginx`: Установка Certbot и его плагина для Nginx.

4. `sudo certbot --nginx -d domain.com -d www.domain.com`: Генерация SSL-сертификата для указанных доменов через Nginx.

5. `certbot renew --dry-run`: Проверка возможности обновления SSL-сертификатов.

6. `sudo nano /etc/nginx/sites-available/default`: Редактирование конфигурационного файла Nginx для настройки SSL-сертификата.

**/etc/nginx/sites-available/default:**
```
server { 
    listen                  443 ssl http2; 
    listen                  [::]:443 ssl http2; 
    server_name             domain.com; 
    # SSL 
    ssl_certificate         /etc/letsencrypt/live/domain.com/fullchain.pem; 
    ssl_certificate_key     /etc/letsencrypt/live/domain.com/privkey.pem; 
    ssl_trusted_certificate /etc/letsencrypt/live/domain.com/chain.pem; 
    include /etc/letsencrypt/options-ssl-nginx.conf; 
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; 
 
    # reverse proxy 
    location / { 
        proxy_pass http://localhost:8000; 
        proxy_http_version 1.1; 
        proxy_set_header Upgrade $http_upgrade; 
        proxy_set_header Connection 'upgrade'; 
        proxy_set_header Host $host; 
        proxy_cache_bypass $http_upgrade; 
    } 
 
} 
 
# subdomains redirect 
server { 
    listen                  443 ssl http2; 
    listen                  [::]:443 ssl http2; 
    server_name             *.domain.com; 
    # SSL 
    ssl_certificate         /etc/letsencrypt/live/domain.com/fullchain.pem; 
    ssl_certificate_key     /etc/letsencrypt/live/domain.com/privkey.pem; 
    ssl_trusted_certificate /etc/letsencrypt/live/domain.com/chain.pem; 
    return                  301 https://**domain.com**$request_uri; 
} 
 
# HTTP redirect 
server { 
    listen      80; 
    listen      [::]:80; 
    server_name .domain.com; 
 
    location / { 
        return 301 https://domain.com$request_uri; 
    } 
}
```
