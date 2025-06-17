# Stage 1: Frontend
FROM node:18 AS frontend
WORKDIR /src/app
COPY package.json yarn.lock ./
COPY .yarn .yarn
COPY .yarnrc.yml ./
RUN yarn install

# Stage 2: Go Builder
FROM golang:1.23 AS builder
ENV GO111MODULE=on
WORKDIR /src/app

COPY --from=frontend /src/app /src/app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# 🟢 Install Buffalo CLI
RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14

# 🟢 Build app binary tanpa --static agar tidak error CGO
RUN buffalo build --skip-assets -o /bin/app

# Final stage: Runtime
FROM alpine:latest

# 🟢 Tambah `git` agar bisa clone di entrypoint.sh
RUN apk add --no-cache bash ca-certificates postgresql-client git dos2unix

WORKDIR /app

# 🟢 Copy binary ke /bin/app
COPY --from=builder /bin/app /bin/app

# 🟢 Simbolik link ke /bin/buffalo agar entrypoint.sh bisa pakai 'buffalo'
RUN ln -s /bin/app /bin/buffalo

# 🟢 Copy entrypoint.sh dan konversi format ke Unix
COPY entrypoint.sh /bin/entrypoint.sh
RUN dos2unix /bin/entrypoint.sh && chmod +x /bin/entrypoint.sh

EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
