# 🚀 NestJS Replication Demo App

This project is a simple NestJS API designed to demonstrate integration with a PostgreSQL master-slave replication setup. It includes basic CRUD endpoints and supports read/write routing between master and slave using TypeORM.

---

## 📦 Features

- NestJS REST API with TypeORM
- Write to `pg-master`, read from `pg-slave`
- Uses `.env` for dynamic configuration
- Dockerized for isolated dev environment
- Includes stress benchmark script (`benchmark.sh`) for load testing
- Compatible with Bitnami PostgreSQL Docker images

---

## 🧱 Folder Structure

```

02-nestjs-replication/
├── app/                # NestJS app source
│   ├── src/
│   ├── Dockerfile
│   ├── .env
│   ├── package.json
│   └── ...
├── docker-compose.yml  # Compose file to run the app container
└── README.md           # This file

````

---

## 🐳 Running with Docker Compose

Make sure your PostgreSQL replication environment is already running  
(e.g. from `01-setup-replication-postgres` with `pg-master` and `pg-slave` containers).

1. Ensure `lab-net` exists:

```bash
docker network create lab-net
````

2. Build and run the NestJS app:

```bash
cd 02-nestjs-replication
docker compose up --build
```

3. API will be available at:

```
http://localhost:3000/messages
```

---

## 🔧 API Endpoints

### `GET /messages`

* Returns all messages (reads from `pg-slave`)

### `POST /messages`

* Creates a new message (writes to `pg-master`)

Body format:

```json
{
  "text": "your message here"
}
```

---

## 🧪 Benchmarking

Run the included `benchmark.sh` script to stress test the API:

```bash
bash benchmark.sh
```

This sends thousands of concurrent requests and logs results (time, size, speed) to `benchmark_log.csv`.

---

## 📝 Notes

* Make sure `.env` or Docker environment matches your DB service names:

  * `pg-master` → write
  * `pg-slave` → read
* TypeORM is configured to connect to both via `TypeOrmModule` + `slaveDataSource`

---

## 📄 License

MIT — feel free to use, modify, or extend for your own database testing.

---

Happy testing! 💥