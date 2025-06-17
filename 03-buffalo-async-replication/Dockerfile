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

RUN go install github.com/gobuffalo/cli/cmd/buffalo@v0.18.14
RUN buffalo build --skip-assets -o /bin/app  # <- tanpa --static

# Final stage: Runtime
FROM alpine:latest
RUN apk add --no-cache bash ca-certificates postgresql-client
WORKDIR /app
COPY --from=builder /bin/app /bin/app
COPY entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
