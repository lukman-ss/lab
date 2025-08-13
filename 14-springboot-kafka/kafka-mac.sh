#!/usr/bin/env bash
# Usage:
#   bash ~/kafka-mac.sh get
#   bash ~/kafka-mac.sh start
#   bash ~/kafka-mac.sh topics
set -e

# Versi Kafka (stabil). Kalau mirror apache lambat, ganti URL ke archive.apache.org
KVER="3.6.1"
KDIR="$HOME/kafka_2.13-$KVER"
CFG="$KDIR/config/kraft/server.properties"
LOGDIR="/tmp/kraft-combined-logs"

get_kafka() {
  cd "$HOME"
  if [ ! -f "kafka_2.13-$KVER.tgz" ]; then
    echo "Downloading Kafka $KVER..."
    curl -fL "https://downloads.apache.org/kafka/$KVER/kafka_2.13-$KVER.tgz" -o "kafka_2.13-$KVER.tgz" || \
    curl -fL "https://archive.apache.org/dist/kafka/$KVER/kafka_2.13-$KVER.tgz" -o "kafka_2.13-$KVER.tgz"
  fi
  rm -rf "$KDIR"
  tar -xzf "kafka_2.13-$KVER.tgz"
  echo "Kafka extracted to $KDIR"
}

write_server_properties() {
  cat > "$CFG" <<'CFGEOF'
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093

listeners=PLAINTEXT://:9092,CONTROLLER://:9093
controller.listener.names=CONTROLLER
inter.broker.listener.name=PLAINTEXT
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1
advertised.listeners=PLAINTEXT://localhost:9092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT

log.dirs=/tmp/kraft-combined-logs
num.partitions=3
auto.create.topics.enable=true

# optional tuning
group.initial.rebalance.delay.ms=0
message.max.bytes=20971520
replica.fetch.max.bytes=20971520
CFGEOF
}

format_storage_if_needed() {
  if [ ! -d "$LOGDIR" ] || [ -z "$(ls -A "$LOGDIR" 2>/dev/null)" ]; then
    echo "Formatting KRaft storage..."
    CLUSTER_ID="$("$KDIR/bin/kafka-storage.sh" random-uuid)"
    "$KDIR/bin/kafka-storage.sh" format -t "$CLUSTER_ID" -c "$CFG"
    echo "Formatted with CLUSTER_ID=$CLUSTER_ID"
  fi
}

case "$1" in
  get)
    get_kafka
    write_server_properties
    echo "Done. Next: bash ~/kafka-mac.sh start"
    ;;
  start)
    [ -d "$KDIR" ] || { echo "Kafka not found. Run: bash ~/kafka-mac.sh get"; exit 1; }
    write_server_properties
    format_storage_if_needed
    echo "Starting Kafka... (keep this terminal open)"
    exec "$KDIR/bin/kafka-server-start.sh" "$CFG"
    ;;
  topics)
    "$KDIR/bin/kafka-topics.sh" --create --if-not-exists --topic payments.requested  --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
    "$KDIR/bin/kafka-topics.sh" --create --if-not-exists --topic payments.completed --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
    "$KDIR/bin/kafka-topics.sh" --list --bootstrap-server localhost:9092
    ;;
  *)
    echo "Usage: bash ~/kafka-mac.sh {get|start|topics}"
    exit 1
    ;;
esac

#!/usr/bin/env bash
# Usage:
#   bash ~/kafka-mac.sh get
#   bash ~/kafka-mac.sh start
#   bash ~/kafka-mac.sh topics
set -e

KVER="3.6.1"
KDIR="$HOME/kafka_2.13-$KVER"
CFG="$KDIR/config/kraft/server.properties"
LOGDIR="/tmp/kraft-combined-logs"

get_kafka() {
  cd "$HOME"
  if [ ! -f "kafka_2.13-$KVER.tgz" ]; then
    echo "Downloading Kafka $KVER..."
    curl -fL "https://downloads.apache.org/kafka/$KVER/kafka_2.13-$KVER.tgz" -o "kafka_2.13-$KVER.tgz" || \
    curl -fL "https://archive.apache.org/dist/kafka/$KVER/kafka_2.13-$KVER.tgz" -o "kafka_2.13-$KVER.tgz"
  fi
  rm -rf "$KDIR"
  tar -xzf "kafka_2.13-$KVER.tgz"
  echo "Kafka extracted to $KDIR"
}

write_server_properties() {
  cat > "$CFG" <<'CFGEOF'
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@localhost:9093

# Listener untuk broker & controller
listeners=PLAINTEXT://:9092,CONTROLLER://:9093
advertised.listeners=PLAINTEXT://localhost:9092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT

# WAJIB di KRaft: nama listener controller harus sesuai dengan 'listeners'
controller.listener.names=CONTROLLER
# Listener antar-broker
inter.broker.listener.name=PLAINTEXT

log.dirs=/tmp/kraft-combined-logs
num.partitions=3
auto.create.topics.enable=true

# Single-node factors
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1

# Tuning ringan
group.initial.rebalance.delay.ms=0
message.max.bytes=20971520
replica.fetch.max.bytes=20971520
CFGEOF
}

format_storage_fresh() {
  # Hapus format lama agar tidak bentrok konfigurasi
  rm -rf "$LOGDIR"
  mkdir -p "$LOGDIR"
  echo "Formatting KRaft storage..."
  CLUSTER_ID="$("$KDIR/bin/kafka-storage.sh" random-uuid)"
  "$KDIR/bin/kafka-storage.sh" format -t "$CLUSTER_ID" -c "$CFG"
  echo "Formatted with CLUSTER_ID=$CLUSTER_ID"
}

case "$1" in
  get)
    get_kafka
    write_server_properties
    echo "Done. Next: bash ~/kafka-mac.sh start"
    ;;
  start)
    [ -d "$KDIR" ] || { echo "Kafka not found. Run: bash $0 get"; exit 1; }
    write_server_properties
    format_storage_fresh
    echo "Starting Kafka... (keep this terminal open)"
    exec "$KDIR/bin/kafka-server-start.sh" "$CFG"
    ;;
  topics)
    "$KDIR/bin/kafka-topics.sh" --create --if-not-exists --topic payments.requested  --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
    "$KDIR/bin/kafka-topics.sh" --create --if-not-exists --topic payments.completed --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
    "$KDIR/bin/kafka-topics.sh" --list --bootstrap-server localhost:9092
    ;;
  *)
    echo "Usage: bash ~/kafka-mac.sh {get|start|topics}"
    exit 1
    ;;
esac
