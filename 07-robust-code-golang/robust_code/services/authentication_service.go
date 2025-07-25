package services

import (
	"errors"
	"time"

	"github.com/gobuffalo/pop/v6"
	"github.com/gofrs/uuid"
	"golang.org/x/crypto/bcrypt"

	"robust_code/models"
)

// AuthenticationService defines auth operations.
type AuthenticationService interface {
	Register(name, email, password string) (*models.User, error)
	Login(email, password string) (*models.User, error)
	Logout(token string) error
}

// PopAuthenticationService implements AuthenticationService with Pop.
type PopAuthenticationService struct {
	db *pop.Connection
}

// NewAuthenticationService returns a new Pop-based auth service.
func NewAuthenticationService(tx *pop.Connection) AuthenticationService {
	return &PopAuthenticationService{db: tx}
}

func (s *PopAuthenticationService) Register(name, email, password string) (*models.User, error) {
	// Email uniqueness
	ex := &models.User{}
	if err := s.db.Where("email = ?", email).First(ex); err == nil {
		return nil, errors.New("email already in use")
	}
	// Hash
	hashed, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}
	// Create
	user := &models.User{
		ID:        uuid.Must(uuid.NewV4()),
		Name:      name,
		Email:     email,
		Password:  string(hashed),
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	if verrs, err := s.db.ValidateAndCreate(user); verrs.HasAny() {
		return nil, errors.New(verrs.Error())
	} else if err != nil {
		return nil, err
	}
	user.Password = ""
	return user, nil
}

func (s *PopAuthenticationService) Login(email, password string) (*models.User, error) {
	user := &models.User{}
	if err := s.db.Where("email = ?", email).First(user); err != nil {
		return nil, errors.New("invalid credentials")
	}
	if bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)) != nil {
		return nil, errors.New("invalid credentials")
	}
	user.Password = ""
	return user, nil
}

func (s *PopAuthenticationService) Logout(token string) error {
	// No-op placeholder
	return nil
}
