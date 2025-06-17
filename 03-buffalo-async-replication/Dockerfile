# Stage 1: Frontend
FROM node:18 AS frontend
WORKDIR /src/app
COPY package.json yarn.lock ./
COPY .yarn .yarn
COPY .yarnrc.yml ./
RUN yarn install

# Stage 2: Build Buffalo App
FROM gobuffalo/buffalo:v0.18.14 AS builder
ENV GOPROXY=https://proxy.golang.org
WORKDIR /src/app
COPY --from=frontend /src/app /src/app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN buffalo build --skip-assets --static -o /bin/app

# Final stage: Runtime
FROM alpine
RUN apk add --no-cache bash ca-certificates postgresql-client
WORKDIR /app
COPY --from=builder /bin/app /bin/app
COPY --from=builder /src/app/entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh
ENV ADDR=0.0.0.0
EXPOSE 3000
CMD ["/bin/entrypoint.sh"]
