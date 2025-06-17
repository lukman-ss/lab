# ========================
# STAGE 1: Builder
# ========================
FROM golang:1.23 AS builder

ENV CGO_ENABLED=0 \
    GO111MODULE=on \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /src/app

# 🟢 Pasang Buffalo CLI
RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14

# 🟢 Copy semua kode
COPY . .

# 🟢 Build langsung pake go build statik, bukan buffalo
RUN go build -o /bin/app

# ========================
# STAGE 2: Runtime Ubuntu
# ========================
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    bash \
    postgresql-client \
    git \
    ca-certificates \
    dos2unix && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /bin/app /bin/app
RUN ln -s /bin/app /bin/buffalo

COPY entrypoint.sh /bin/entrypoint.sh
RUN dos2unix /bin/entrypoint.sh && chmod +x /bin/entrypoint.sh

EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
