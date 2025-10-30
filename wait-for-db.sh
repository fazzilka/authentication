#!/usr/bin/env bash
set -e

host="${DB_HOST:-db}"
port="${DB_PORT:-5432}"
user="${DB_USER:-postgres}"
db="${DB_NAME:-app}"

echo "⏳ Жду Postgres на $host:$port…"
for i in {1..60}; do
  if PGPASSWORD="${DB_PASSWORD:-postgres}" \
     psql "host=$host port=$port user=$user dbname=$db" -c '\q' 2>/dev/null; then
    echo "✅ Postgres доступен."
    exec "$@"
  fi
  sleep 1
done

echo "❌ Не дождался Postgres."
exit 1
