# This is a multi-stage Dockerfile and requires >= Docker 17.05
FROM gobuffalo/buffalo:v0.18.14 as builder

ENV GOPROXY http://proxy.golang.org

RUN mkdir -p /src/03-buffalo-async-replication
WORKDIR /src/03-buffalo-async-replication

ADD package.json .
ADD yarn.lock .
RUN yarn install

COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download

ADD . .
RUN buffalo build --static -o /bin/app

FROM alpine
RUN apk add --no-cache bash
RUN apk add --no-cache ca-certificates

WORKDIR /bin/

COPY --from=builder /bin/app .
COPY entrypoint.sh /bin/entrypoint.sh
RUN chmod +x /bin/entrypoint.sh

ENV ADDR=0.0.0.0

EXPOSE 3000

CMD ["./entrypoint.sh"]
