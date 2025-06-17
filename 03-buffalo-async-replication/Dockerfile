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

# 🟢 Salin source
COPY --from=frontend /src/app /src/app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# 🟢 Install Buffalo CLI (binary ada di /go/bin/buffalo)
RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14

# 🟢 Build binary app ke path berbeda
RUN buffalo build --skip-assets -o /src/app/bin/app

# Stage 3: Runtime
FROM alpine:latest
RUN apk add --no-cache bash ca-certificates postgresql-client git dos2unix

WORKDIR /app

# 🟢 Salin binary Buffalo CLI ke runtime container
COPY --from=builder /go/bin/buffalo /bin/buffalo

# 🟢 Salin hasil build app
COPY --from=builder /src/app/bin/app /bin/app

# 🟢 Salin entrypoint dan ubah format ke Unix
COPY entrypoint.sh /bin/entrypoint.sh
RUN dos2unix /bin/entrypoint.sh && chmod +x /bin/entrypoint.sh

EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
