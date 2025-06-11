🔥 SIAP BRO. Let's clean it up — here's your **FINAL `README.md`**, 100% in **English**, formatted properly, fully consistent with your original intent, and ready for GitHub or any production use:

---

````md
# 🐘 PostgreSQL Master-Slave Replication with Docker Compose (Windows PowerShell)

This guide sets up PostgreSQL streaming replication (master-slave) using Docker Compose, powered by the Bitnami PostgreSQL image. Perfect for development and load testing environments.

---

## ✅ Prerequisites

- Windows with **Docker** and **Docker Compose** installed
- PowerShell or Git Bash
- A Docker network named `lab-net` must be created:

```bash
docker network create lab-net
````

---

## 📁 Directory Structure

```
01-setup-replication-postgres/
├── docker-compose.yml
├── README.md
└── (data is stored in Docker volumes, not inside the project folder)
```

---

## 🐳 docker-compose.yml

```yaml
version: '3.8'

services:
  pg-master:
    image: bitnami/postgresql:14
    container_name: pg-master
    environment:
      - POSTGRESQL_REPLICATION_MODE=master
      - POSTGRESQL_REPLICATION_USER=replicator
      - POSTGRESQL_REPLICATION_PASSWORD=example
      - POSTGRESQL_PASSWORD=example
    volumes:
      - master_data:/bitnami/postgresql
    ports:
      - '5432:5432'
    networks:
      - lab-net

  pg-slave:
    image: bitnami/postgresql:14
    container_name: pg-slave
    depends_on:
      - pg-master
    environment:
      - POSTGRESQL_REPLICATION_MODE=slave
      - POSTGRESQL_REPLICATION_USER=replicator
      - POSTGRESQL_REPLICATION_PASSWORD=example
      - POSTGRESQL_PASSWORD=example
      - POSTGRESQL_MASTER_HOST=pg-master
      - POSTGRESQL_MASTER_PORT_NUMBER=5432
    volumes:
      - slave_data:/bitnami/postgresql
    ports:
      - '5433:5432'
    networks:
      - lab-net

volumes:
  master_data:
  slave_data:

networks:
  lab-net:
    external: true
```

---

## 🚀 How to Run

1. (Optional) Clean up any previous containers and volumes:

```bash
docker compose down -v
```

2. Start the replication cluster:

```bash
docker compose up -d
```

3. Verify running containers:

```bash
docker ps --filter "name=pg-"
```

4. Check replication status on the master:

```bash
docker exec -e PGPASSWORD=example -u postgres pg-master \
  psql -h 127.0.0.1 -U postgres -d postgres \
  -c "SELECT pid, state, client_addr FROM pg_stat_replication;"
```

5. Check recovery mode on the slave:

```bash
docker exec -e PGPASSWORD=example -u postgres pg-slave \
  psql -h 127.0.0.1 -U postgres -d postgres \
  -c "SELECT pg_is_in_recovery();"
```

---

## 🔗 Connection Info

* `localhost:5432` → write DB (pg-master)
* `localhost:5433` → read-only DB (pg-slave)

---

## 🧼 Cleanup

To stop and remove everything including volumes:

```bash
docker compose down -v
```

---

## 📝 Notes

* Passwords are set to `example` for demo purposes. Change them for production use.
* Bitnami PostgreSQL images automatically configure replication via environment variables.
* To view logs:

```bash
docker logs pg-master
docker logs pg-slave
```

---

Happy replicating! 🚀

```