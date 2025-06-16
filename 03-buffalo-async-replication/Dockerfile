FROM golang:1.21

# Install Buffalo CLI
RUN go install github.com/gobuffalo/cli/cmd/buffalo@latest

ENV PATH="/go/bin:${PATH}"
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 3000
CMD ["/entrypoint.sh"]
