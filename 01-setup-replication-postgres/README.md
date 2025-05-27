# PostgreSQL Master-Slave Replication with Docker Compose (Windows PowerShell)

This guide walks through setting up a PostgreSQL streaming replication (master-slave) environment using Docker Compose on Windows PowerShell, leveraging the Bitnami PostgreSQL image for simplicity.

---

## Prerequisites

* Windows with Docker and Docker Compose installed
* PowerShell (as Administrator recommended)
* Basic familiarity with Docker and PostgreSQL

---

## Directory Structure

text
pg-replication/
├── docker-compose.yml
├── master_data/          ← Named volume mount for master data
├── slave_data/           ← Named volume mount for slave data
└── README.md             ← This file


> **Note:** No additional configuration files are required—Bitnami handles initialization.

---

## docker-compose.yml

yaml
services:
  pg-master:
    image: bitnami/postgresql:14
    container_name: pg-master
    environment:
      - POSTGRESQL_REPLICATION_MODE=master
      - POSTGRESQL_REPLICATION_USER=replicator
      - POSTGRESQL_REPLICATION_PASSWORD=example
      - POSTGRESQL_PASSWORD=example
      - POSTGRESQL_DATABASE=postgres
    volumes:
      - master_data:/bitnami/postgresql
    ports:
      - '5432:5432'

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
      - POSTGRESQL_DATABASE=postgres
    volumes:
      - slave_data:/bitnami/postgresql
    ports:
      - '5433:5432'

volumes:
  master_data:
  slave_data:


---

## Steps to Run

1. **Clean up any existing setup** (optional):

   
powershell
   docker-compose down --remove-orphans -v


2. **Bring up the master and slave**:

   
powershell
   docker-compose up -d


3. **Verify containers are running**:

   
powershell
   docker ps --filter "name=pg-"


4. **Check replication status on master**:

   
powershell
   docker exec -e PGPASSWORD=example -u postgres pg-master psql \
     -h 127.0.0.1 -U postgres -d postgres -c "SELECT pid, state, client_addr FROM pg_stat_replication;"


5. **Check recovery mode on slave**:

   
powershell
   docker exec -e PGPASSWORD=example -u postgres pg-slave psql \
     -h 127.0.0.1 -U postgres -d postgres -c "SELECT pg_is_in_recovery();"


---

## Usage

* Connect to **master** on localhost:5432 for read-write operations.
* Connect to **slave** on localhost:5433 for read-only reports or load balancing.

---

## Cleanup

To stop and remove all resources, run:

powershell
docker-compose down -v


---

## Notes

* Default passwords are set to example for demo purposes—change them in production.
* Bitnami images handle replication setup automatically via environment variables.
* Logs can be viewed with docker logs pg-master and docker logs pg-slave.

---

Happy replicating! 0🚀 