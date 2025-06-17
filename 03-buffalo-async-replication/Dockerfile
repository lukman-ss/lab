# Stage 1: Frontend
FROM node:18 AS frontend
WORKDIR /src/app

# Salin file konfigurasi dan install dependencies frontend
COPY package.json yarn.lock ./
COPY .yarn .yarn
COPY .yarnrc.yml ./
RUN yarn install

# Stage 2: Go Builder
FROM golang:1.23 AS builder
ENV GO111MODULE=on
WORKDIR /src/app

# Salin hasil dari frontend dan mod files
COPY --from=frontend /src/app /src/app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# Install Buffalo CLI dan build aplikasi
RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14
RUN buffalo build --skip-assets -o /bin/app  # Tanpa --static agar tidak error CGO

# Stage 3: Final Runtime
FROM alpine:latest
# Install tool yang diperlukan + dos2unix untuk perbaikan format shell script
RUN apk add --no-cache bash ca-certificates postgresql-client dos2unix git 

WORKDIR /app

# Copy binary hasil build dan entrypoint script
COPY --from=builder /bin/app /bin/app
COPY entrypoint.sh /bin/entrypoint.sh

# Ubah format Windows ke Unix (CRLF -> LF) dan beri permission eksekusi
RUN dos2unix /bin/entrypoint.sh && chmod +x /bin/entrypoint.sh

EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
