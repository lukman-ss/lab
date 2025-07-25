package authentication

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"robust_code/models"
	"robust_code/requests"

	auth "robust_code/actions/api/authentication"

	"github.com/gobuffalo/pop/v6"
	"github.com/gofrs/uuid"
	"github.com/stretchr/testify/require"
	"golang.org/x/crypto/bcrypt"
)

// reset the users table between tests
func resetDB(t *testing.T) {
	tx := models.DB
	_, err := tx.RawQuery("TRUNCATE TABLE users RESTART IDENTITY CASCADE").Exec()
	require.NoError(t, err)
}

func Test_Register(t *testing.T) {
	resetDB(t)
	app := App() // import your Buffalo app

	payload := `{"name":"Alice","email":"a@b.com","password":"secret123"}`
	req := httptest.NewRequest("POST", "/api/auth/register", strings.NewReader(payload))
	req.Header.Set("Content-Type", "application/json")
	res := httptest.NewRecorder()
	app.ServeHTTP(res, req)

	require.Equal(t, http.StatusCreated, res.Code)
	require.Contains(t, res.Body.String(), `"email":"a@b.com"`)
}

func Test_Login(t *testing.T) {
	resetDB(t)
	// seed a user
	tx := models.DB
	hashed, _ := bcrypt.GenerateFromPassword([]byte("secret123"), bcrypt.DefaultCost)
	u := &models.User{
		ID:        uuid.Must(uuid.NewV4()),
		Name:      "Bob",
		Email:     "bob@c.com",
		Password:  string(hashed),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	require.NoError(t, tx.Create(u))

	app := App()
	payload := `{"email":"bob@c.com","password":"secret123"}`
	req := httptest.NewRequest("POST", "/api/auth/login", strings.NewReader(payload))
	req.Header.Set("Content-Type", "application/json")
	res := httptest.NewRecorder()
	app.ServeHTTP(res, req)

	require.Equal(t, http.StatusOK, res.Code)
	require.Contains(t, res.Body.String(), `"email":"bob@c.com"`)
}

func Test_Logout(t *testing.T) {
	app := App()
	req := httptest.NewRequest("POST", "/api/auth/logout", strings.NewReader(`{"token":"abc"}`))
	req.Header.Set("Content-Type", "application/json")
	res := httptest.NewRecorder()
	app.ServeHTTP(res, req)

	require.Equal(t, http.StatusOK, res.Code)
	require.Contains(t, res.Body.String(), `"message":"logged out"`)
}
