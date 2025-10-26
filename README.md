# FastAPI + AuthX Starter


Аутентификация на **FastAPI + AuthX + SQLAlchemy (async)** с безопасными паролями (**Argon2 / pwdlib**), схемами на **Pydantic v2**, Postgres и удобным запуском через **uv** и **Docker Compose**.


## 🔧 Стек
- FastAPI, Uvicorn
- AuthX (JWT, access/refresh)
- SQLAlchemy 2.0 (async) + asyncpg
- Pydantic v2, pydantic-settings
- Argon2 (pwdlib)
- Docker + Docker Compose (dev)
- uv (управление окружением/зависимостями)


## 📁 Структура

app/ api/ routes/ auth.py users.py auth/ deps.py jwt.py core/ config.py security.py db/ base.py session.py models/ user.py repositories/ users.py schemas/ auth.py user.py main.py

.env.example pyproject.toml (или requirements.txt) Dockerfile docker-compose.yml .dockerignore



## ⚙️ Переменные окружения
Скопируй `.env.example` → `.env` и заполни:
```dotenv
# JWT
JWT_SECRET_KEY=change-me-super-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MIN=15
REFRESH_TOKEN_EXPIRES_DAYS=7


# Database (локально через Docker Compose см. ниже будет другой URL)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app


APP_NAME=AuthX Starter
APP_DEBUG=true
▶️ Запуск через uv (локально)
Установка uv (один раз)
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
Быстрый старт (без ручной активации venv)
cp .env.example .env
uv run --env-file .env uvicorn app.main:app --reload
Классический режим
uv venv --python 3.11
uv sync
# (опционально) source .venv/bin/activate
uv run --env-file .env uvicorn app.main:app --reload
🐘 PostgreSQL
Вариант A — Docker (проще всего)
docker compose up --build
# API: http://127.0.0.1:8000/docs

В docker-compose.yml сервис app использует DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app — хост db это имя сервиса внутри сети Compose.

Вариант B — native (Linux/Fedora)

Установи postgresql-server, создай пользователя/базу и укажи локальный DATABASE_URL в .env.

🚦 API — основные маршруты

POST /auth/register — регистрация { email, password }

POST /auth/login — логин → { access_token, refresh_token }

POST /auth/refresh — новый access-токен по refresh

GET /users/me — защищённый профиль по Authorization: Bearer <access>

🔍 Примеры запросов
curl
curl -X POST :8000/auth/register -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"YourStrongPassw0rd!"}'


curl -X POST :8000/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"YourStrongPassw0rd!"}'


ACCESS=... # подставь из login
curl :8000/users/me -H "Authorization: Bearer $ACCESS"


REFRESH=... # подставь из login
curl -X POST :8000/auth/refresh -H "Authorization: Bearer $REFRESH"
HTTPie
http POST :8000/auth/register email==you@example.com password==YourStrongPassw0rd!
http POST :8000/auth/login    email==you@example.com password==YourStrongPassw0rd!
http GET  :8000/users/me Authorization:"Bearer <ACCESS>"
http POST :8000/auth/refresh  Authorization:"Bearer <REFRESH>"
🧪 Миграции (опционально)

Для продакшена подключите Alembic, вместо авто‑создания таблиц на старте:

uv add alembic
uv run alembic init -t async migrations
# настройте sqlalchemy.url и env.py, затем
uv run alembic revision -m "init"
uv run alembic upgrade head
🐳 Docker Compose — команды
docker compose up --build       # собрать и запустить
docker compose up -d            # запустить в фоне
docker compose down             # остановить
docker compose down -v          # остановить и удалить volume с данными БД
🛡 Безопасность

Пароли хэшируются Argon2 (pwdlib). Сырые пароли не храним.

Секреты JWT — только через .env/переменные окружения.

В проде: без --reload, используйте gunicorn/uvicorn workers, TLS (через nginx/traefik), CORS, rate limits.

🆘 Частые проблемы:

FATAL: Peer/Ident authentication failed — проверь pg_hba.conf (метод md5/scram-sha-256) и перезапусти Postgres.

OperationalError: connection refused — проверь, что Postgres запущен и DATABASE_URL корректен.

409 Email already registered — email занят.

401 Invalid credentials — неправильный email/пароль.

401 User not found — в токене sub несуществующий пользователь (например, удалён).
