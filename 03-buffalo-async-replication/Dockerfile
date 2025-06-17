# ========================
# STAGE 1: Builder
# ========================
FROM golang:1.21 AS builder

# 🟢 Konfigurasi agar hasil build statik dan bisa jalan di Alpine
ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

WORKDIR /src/app

# 🟢 Install Buffalo CLI
RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14

# 🟢 Copy semua source code
COPY . .

# 🟢 Build binary statik agar tidak error "not found" di Alpine
RUN /go/bin/buffalo build --static --skip-assets -o /bin/app


# ========================
# STAGE 2: Runtime
# ========================
FROM alpine:latest

# 🟢 Install tools penting
RUN apk add --no-cache bash postgresql-client git ca-certificates

WORKDIR /app

# 🟢 Salin binary dari builder
COPY --from=builder /bin/app /bin/app

# 🟢 Alias simbolik ke `buffalo`
RUN ln -s /bin/app /bin/buffalo

# 🟢 Salin dan aktifkan entrypoint
COPY entrypoint.sh /bin/entrypoint.sh
RUN dos2unix /bin/entrypoint.sh && chmod +x /bin/entrypoint.sh

EXPOSE 3000

CMD ["/bin/entrypoint.sh"]
