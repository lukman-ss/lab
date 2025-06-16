#!/bin/bash

# Cek apakah file utama sudah ada
if [ ! -f /app/main.go ]; then
  echo "🌀 Project belum ada, cloning..."
  git clone https://github.com/lukman-ss/lab.git /tmp/lab

  mkdir -p /app
  mv /tmp/lab/03-buffalo-async-replication/* /app/
  mv /tmp/lab/03-buffalo-async-replication/.* /app/ 2>/dev/null || true

  rm -rf /tmp/lab
else
  echo "✅ Project sudah ada, skip git clone"
fi

# Masuk ke direktori dan jalankan server
cd /app
buffalo dev
