
# Payment Service

The **Payment Service** listens for **`PaymentRequestedEvent`** messages from Kafka, processes the payment (simulation), and publishes a **`PaymentResultEvent`** to another topic.

## Configuration
`application.yml`:
```yaml
server:
  port: 8081
app:
  topics:
    paymentRequested: payments.requested
    paymentCompleted: payments.completed
spring:
  kafka:
    bootstrap-servers: localhost:9092
````

## Run the Service

```bash
./mvnw spring-boot:run
```

## Flow

1. `PaymentRequestConsumer` consumes `PaymentRequestedEvent`.
2. The service simulates payment processing.
3. `PaymentResultProducer` publishes `PaymentResultEvent` to the `payments.completed` topic.

## Package Structure

```
com.techthinkhub.payment
├─ dto/              # DTOs for events
└─ kafka/            # Kafka consumer and producer
```
