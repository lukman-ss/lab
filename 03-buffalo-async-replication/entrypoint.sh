#!/bin/bash
set -e

# Clone project jika belum ada
if [ ! -f /app/main.go ]; then
  echo "🌀 Cloning project dari GitHub..."
  git clone https://github.com/lukman-ss/lab.git /tmp/lab
  cp -r /tmp/lab/03-buffalo-async-replication/. /app/
  rm -rf /tmp/lab
else
  echo "✅ Project sudah ada, skip clone"
fi

cd /app

# Tunggu PostgreSQL master siap
echo "⏳ Menunggu database..."
until pg_isready -h postgre-sync-master -p 5432 -U postgres; do
  sleep 1
done

export DATABASE_URL=postgres://postgres:example@postgre-sync-master:5432/postgres?sslmode=disable

# Jalankan migrasi
echo "⚙️  Menjalankan migrasi..."
buffalo pop migrate

# Jalankan aplikasi
echo "🚀 Menjalankan Buffalo Dev..."
buffalo dev
