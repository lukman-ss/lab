# ========================
# STAGE 1: Builder
# ========================
FROM golang:1.23 AS builder

ENV CGO_ENABLED=0 \
    GO111MODULE=on \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /src/app

# Install Buffalo CLI
RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14

# Clone source code
RUN git clone https://github.com/lukman-ss/lab.git /tmp/lab
RUN cp -r /tmp/lab/03-buffalo-async-replication/. /src/app/

# Build static binary
RUN /go/bin/buffalo build --static --skip-assets -o /bin/app

# ========================
# STAGE 2: Runtime (Ubuntu)
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

# Copy binary dari builder
COPY --from=builder /bin/app /bin/app

# Optional: symbolic link
RUN ln -s /bin/app /bin/buffalo

# Copy entrypoint
COPY entrypoint.sh /bin/entrypoint.sh
RUN dos2unix /bin/entrypoint.sh && chmod +x /bin/entrypoint.sh

EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
