#!/bin/bash
# Скрипт установки Second_life на Ubuntu-сервере
# Запуск: bash deploy_server.sh

set -e

PROJECT_DIR="$HOME/Second_life"
DB_NAME="web_second_life"
DB_USER="postgres"

echo "=== 1. Системные пакеты ==="
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv \
    postgresql postgresql-contrib libpq-dev python3-dev build-essential

echo "=== 2. PostgreSQL ==="
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Создать БД, если нет
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 \
    || sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"

echo "=== 3. Проект ==="
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ОШИБКА: папка $PROJECT_DIR не найдена!"
    echo "Сначала загрузи проект в ~/Second_life"
    exit 1
fi

cd "$PROJECT_DIR"

echo "=== 4. config.py ==="
if [ ! -f "config.py" ]; then
    echo "ОШИБКА: нет config.py в $PROJECT_DIR"
    echo "Создай файл:"
    echo "  nano config.py"
    echo "С содержимым:"
    echo "  SECRET_KEY = 'случайная-строка'"
    echo "  PASSWORD_POSTGRESQL = 'пароль_postgres'"
    exit 1
fi

# Проверка кодировки requirements.txt
if file requirements.txt | grep -q UTF-16; then
    echo "Исправляю кодировку requirements.txt (UTF-16 -> UTF-8)..."
    iconv -f UTF-16LE -t UTF-8 requirements.txt -o requirements_fixed.txt
    mv requirements_fixed.txt requirements.txt
fi

echo "=== 5. Виртуальное окружение ==="
python3 -m venv env
source env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "=== 6. Миграции ==="
export FLASK_APP=webapp
alembic upgrade head

echo "=== 7. Проверка ==="
python3 -c "from config import PASSWORD_POSTGRESQL; from webapp import app; print('OK: приложение загружается')"

echo ""
echo "=== ГОТОВО ==="
echo "Запуск сервера:"
echo "  cd ~/Second_life"
echo "  source env/bin/activate"
echo "  export FLASK_APP=webapp"
echo "  flask run --host=0.0.0.0 --port=5000"
echo ""
echo "Открой в браузере: http://ВАШ_IP:5000"
echo "Не забудь открыть порт 5000 в группе безопасности Yandex Cloud!"
