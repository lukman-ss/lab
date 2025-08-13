# Checkout Service

The **Checkout Service** is responsible for creating new orders and publishing a **`PaymentRequestedEvent`** to Kafka.  
It also consumes **`PaymentResultEvent`** from Kafka to update the order status.

## Configuration
`application.yml`:
```yaml
server:
  port: 8080
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

## API Endpoint

* **POST** `/checkout`
  **Request Body:**

  ```json
  {
    "orderId": "ORD-001",
    "amount": 150000
  }
  ```

## Package Structure

```
com.techthinkhub.checkout
├─ domain/           # Order status enum
├─ dto/              # DTOs for events and requests
├─ kafka/            # Kafka producer and consumer
├─ repo/             # Temporary order storage
└─ web/              # REST controller
```

