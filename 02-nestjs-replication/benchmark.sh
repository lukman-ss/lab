#!/bin/bash

# Konfigurasi
REQUESTS=2000
CONCURRENT=100
URL="http://localhost:3000/messages"
CSV_FILE="benchmark_log.csv"
TIMESTAMP=$(date -Iseconds)

# Header CSV kalau belum ada
if [ ! -f "$CSV_FILE" ]; then
  echo "timestamp,requests,concurrent,duration_sec,size_bytes,speed_bps,time_total,code" >> "$CSV_FILE"
fi

echo "🔥 Mulai stress test: $REQUESTS POST (concurrent $CONCURRENT)"
start_time=$SECONDS

# Kirim POST request
seq 1 $REQUESTS | xargs -P $CONCURRENT -I {} curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Lorem ipsum {}\"}" > /dev/null

duration=$((SECONDS - start_time))
echo "✅ POST selesai dalam ${duration}s"
echo ""

# Ambil hasil GET + parsing metrik
result=$(curl -s -w "%{size_download},%{speed_download},%{time_total},%{http_code}" -o /dev/null "$URL")
IFS=',' read -r size speed time code <<< "$result"

# Simpan ke CSV
echo "$TIMESTAMP,$REQUESTS,$CONCURRENT,$duration,$size,$speed,$time,$code" >> "$CSV_FILE"

# Tampilkan juga ke terminal
echo "📥 Benchmark hasil:"
echo "📦 Size: $size bytes"
echo "🚀 Speed: $speed B/s"
echo "⏱ Time Total: $time s"
echo "🔗 HTTP Code: $code"
echo "📊 Data disimpan di: $CSV_FILE"
