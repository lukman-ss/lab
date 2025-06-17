# ========================
# STAGE 1: Builder
# ========================
FROM golang:1.21 AS builder

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /src/app

RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14

COPY . .
RUN /go/bin/buffalo build --static --skip-assets -o /bin/app

# ========================
# STAGE 2: Runtime (Ubuntu)
# ========================
FROM ubuntu:22.04

# Install tools
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
