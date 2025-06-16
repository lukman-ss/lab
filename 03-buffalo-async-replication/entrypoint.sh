#!/bin/bash

# Cek apakah main.go ada
if [ ! -f /app/main.go ]; then
  echo "🌀 Project belum ada, cloning dari repo..."
  git clone https://github.com/lukman-ss/lab.git /tmp/lab

  mkdir -p /app
  cp -r /tmp/lab/03-buffalo-async-replication/. /app/
  rm -rf /tmp/lab
else
  echo "✅ Project sudah ada, skip git clone"
fi

cd /app

# Tunggu database siap
echo "⏳ Menunggu database..."
until pg_isready -h postgre-sync-master -p 5432 -U postgres; do
  sleep 1
done

# Jalankan migrasi (optional)
echo "⚙️  Menjalankan migrasi database..."
buffalo pop migrate

# Jalankan aplikasi
echo "🚀 Menjalankan Buffalo dev..."
buffalo dev
