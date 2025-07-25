package repositories

import (
	"robust_code/models"

	"github.com/gobuffalo/pop/v6"
)

// PopUserRepository implements UserRepository using Pop.
type PopUserRepository struct {
	tx *pop.Connection
}

// NewPopUserRepository returns a new PopUserRepository.
func NewPopUserRepository(tx *pop.Connection) *PopUserRepository {
	return &PopUserRepository{tx: tx}
}

func (r *PopUserRepository) FindAll() ([]models.User, error) {
	var users []models.User
	if err := r.tx.All(&users); err != nil {
		return nil, err
	}
	return users, nil
}

func (r *PopUserRepository) FindByID(id string) (*models.User, error) {
	u := &models.User{}
	if err := r.tx.Find(u, id); err != nil {
		return nil, err
	}
	return u, nil
}

func (r *PopUserRepository) FindByEmail(email string) (*models.User, error) {
	u := &models.User{}
	if err := r.tx.Where("email = ?", email).First(u); err != nil {
		return nil, err
	}
	return u, nil
}

func (r *PopUserRepository) Create(user *models.User) error {
	return r.tx.Create(user)
}

func (r *PopUserRepository) Update(user *models.User) error {
	return r.tx.Update(user)
}

func (r *PopUserRepository) Delete(user *models.User) error {
	return r.tx.Destroy(user)
}
