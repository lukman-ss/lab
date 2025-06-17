# ======================== 
# STAGE 1: Builder 
# ======================== 
FROM golang:1.21 AS builder

ENV GO111MODULE=on
WORKDIR /src/app

# 🟢 Install Buffalo CLI ke /go/bin
RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14

# 🟢 Copy semua kode
COPY . .

# 🟢 Install dep
RUN go mod tidy

# 🟢 Build Buffalo project
RUN /go/bin/buffalo build --static --skip-assets -o /bin/buffalo

# ========================
# STAGE 2: Runtime
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

# 🟢 Salin hasil build buffalo
COPY --from=builder /bin/buffalo /bin/buffalo

# 🟢 Salin script entrypoint
COPY entrypoint.sh /bin/entrypoint.sh
RUN dos2unix /bin/entrypoint.sh && chmod +x /bin/entrypoint.sh

EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
