# Product API (Spring Boot 3, Java 21)

A simple CRUD API for managing products with in-memory storage.
Built with Spring Boot 3.x and Java 21.

## Features
- Create, Read, Update, Delete products
- Auto-incrementing IDs (in memory)
- DevTools for hot reload during development

## Stack
- Java 21
- Spring Boot 3.x (`spring-boot-starter-web`, `spring-boot-devtools`)
- Maven Wrapper (`mvnw`)

## Prerequisites
- JDK 21 installed (`java -version`)
- Default port: `8080`

## Run the Application
```bash
./mvnw spring-boot:run
# or build a jar:
./mvnw -q package
java -jar target/product-api-0.0.1-SNAPSHOT.jar
````

## Endpoints

Base path: `/api/products`

| Method | Path                 | Description    |
| -----: | -------------------- | -------------- |
|    GET | `/api/products`      | List products  |
|    GET | `/api/products/{id}` | Get by ID      |
|   POST | `/api/products`      | Create product |
|    PUT | `/api/products/{id}` | Full update    |
| DELETE | `/api/products/{id}` | Delete product |

### cURL Examples

Create:

```bash
curl -s -X POST http://localhost:8080/api/products \
  -H 'Content-Type: application/json' \
  -d '{"name":"Shirt","price":150000,"stock":10}'
```

List:

```bash
curl -s http://localhost:8080/api/products
```

Get by ID:

```bash
curl -s http://localhost:8080/api/products/1
```

Update:

```bash
curl -i -X PUT http://localhost:8080/api/products/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Shirt XL","price":160000,"stock":8}'
```

Delete:

```bash
curl -i -X DELETE http://localhost:8080/api/products/1
```

## Project Structure

```
product-api
├─ .mvn/wrapper/maven-wrapper.properties
├─ README.md
├─ mvnw / mvnw.cmd
├─ pom.xml
└─ src
   ├─ main
   │  ├─ java/com/techthinkhub/productapi
   │  │  ├─ Product.java
   │  │  ├─ ProductApiApplication.java
   │  │  └─ ProductController.java
   │  └─ resources
   │     ├─ application.properties
   │     ├─ static/
   │     └─ templates/
   └─ test/java/com/techthinkhub/productapi/ProductApiApplicationTests.java
```

## Configuration

Change the port in `src/main/resources/application.properties`:

```properties
# server.port=8081
```

## Notes

* Data is stored in memory and will be lost when the application stops. For persistence, add JPA and a database (H2 or PostgreSQL).
* Validation is minimal and intended for demonstration.