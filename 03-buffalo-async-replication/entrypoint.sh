#!/bin/sh
set -e

# Clone ulang (kalau dijalankan tanpa tahap clone di builder)
if [ ! -f /app/main.go ]; then
  echo "🌀 Cloning project dari GitHub..."
  git clone https://github.com/lukman-ss/lab.git /tmp/lab
  cp -r /tmp/lab/03-buffalo-async-replication/. /app/
  rm -rf /tmp/lab
else
  echo "✅ Project sudah ada, skip clone"
fi

cd /app

echo "⏳ Menunggu database..."
until pg_isready -h postgre-sync-master -p 5432 -U postgres; do
  sleep 1
done

export DATABASE_URL=postgres://postgres:example@postgre-sync-master:5432/postgres?sslmode=disable

echo "⚙️  Menjalankan migrasi..."
/bin/app pop migrate

echo "🚀 Menjalankan Buffalo Dev..."
exec /bin/app dev
