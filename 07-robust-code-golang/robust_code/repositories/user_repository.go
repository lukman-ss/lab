package repositories

import (
	"robust_code/models"
)

// UserRepository defines data‐access methods for User.
type UserRepository interface {
	FindAll() ([]models.User, error)
	FindByID(id string) (*models.User, error)
	FindByEmail(email string) (*models.User, error)
	Create(user *models.User) error
	Update(user *models.User) error
	Delete(user *models.User) error
}
