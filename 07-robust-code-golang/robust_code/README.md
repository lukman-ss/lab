````markdown
# Robust Code Buffalo API

Proyek ini mengeksplorasi arsitektur “robust code” pada aplikasi Go menggunakan [Buffalo](https://gobuffalo.io). Anda akan menemukan pemisahan tanggung jawab ke dalam layer:

- **Actions**: HTTP handlers & routing  
- **Models**: definisi Pop model (`User`)  
- **Repositories**: interface + implementasi data access (Pop)  
- **Validation (Requests)**: FormRequest structs & field-level validation  
- **Services**: logika bisnis (pendaftaran, login, logout)  
- **Resource**: Buffalo Resource untuk CRUD otomatis  

---

## Prerequisites

- Go 1.24.5  
- Buffalo CLI (`go install github.com/gobuffalo/cli/cmd/buffalo@latest`)  
- PostgreSQL (atau database lain sesuai konfigurasi env)  

---

## Instalasi

1. **Clone** repo  
   ```bash
   git clone https://github.com/lukman-ss/lab.git
   cd 07-robust-code-golang/robust_code
````

2. **Setup environment**
   Copy `.env.example` ke `.env` dan sesuaikan `DATABASE_URL`:

   ```dotenv
   DATABASE_URL=postgres://root:postgres@127.0.0.1:55444/robust_code?sslmode=disable
   ```
3. **Install dependencies & migrasi**

   ```bash
   go mod tidy
   buffalo pop migrate
   ```

---

## Struktur Direktori

```
.
├── actions/               
│   └── api/
│       └── authentication/
│           └── authentication.go   # Register/Login/Logout handlers
├── models/
│   └── user.go                     # Pop model
├── repositories/
│   ├── user_repository.go         # interface
│   └── pop_user_repository.go     # Pop impl
├── requests/
│   └── authentication_request.go  # FormRequest & validation
├── resource/
│   └── user_resource.go           # Buffalo Resource CRUD /api/users
├── services/
│   └── authentication_service.go  # business logic
├── migrations/                    # Fizz migration files
├── actions/app.go                 # Buffalo app setup & route mounting
├── go.mod
└── README.md
```

---

## Menjalankan Server

```bash
buffalo dev
```

Server akan berjalan di `http://localhost:3000`.

---

## Endpoints

### Authentication

| Method | Path                 | Deskripsi        |
| ------ | -------------------- | ---------------- |
| POST   | `/api/auth/register` | Daftar user baru |
| POST   | `/api/auth/login`    | Login user       |
| POST   | `/api/auth/logout`   | Logout (stub)    |

**Contoh Payload Register**

```json
{
  "name": "Nama Lengkap",
  "email": "user@example.com",
  "password": "minimal6karakter"
}
```

**Contoh Payload Login**

```json
{
  "email": "user@example.com",
  "password": "minimal6karakter"
}
```

---

### User CRUD Resource

| Method | Path                   | Deskripsi        |
| ------ | ---------------------- | ---------------- |
| GET    | `/api/users`           | Ambil semua user |
| POST   | `/api/users`           | Buat user baru   |
| GET    | `/api/users/{user_id}` | Ambil user by ID |
| PUT    | `/api/users/{user_id}` | Update data user |
| DELETE | `/api/users/{user_id}` | Hapus user       |

**Contoh Create User**

```json
POST /api/users
{
  "name": "Budi",
  "email": "budi@example.com",
  "password": "secret123"
}
```

---

## Testing

```bash
buffalo test
```

Suite mencakup unit tests untuk:

* FormRequest validation
* Service layer (Register/Login/Logout)
* Resource CRUD

---

## Lisensi

MIT © Lukman

```
::contentReference[oaicite:0]{index=0}
```
