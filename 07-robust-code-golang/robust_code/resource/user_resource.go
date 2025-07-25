package resource

import (
	"net/http"

	"github.com/gobuffalo/buffalo"
	"github.com/gobuffalo/buffalo/render"
	"github.com/gobuffalo/pop/v6"

	"robust_code/models"
	"robust_code/repositories"
)

// UserResource implements buffalo.Resource for /api/users
type UserResource struct {
	repo repositories.UserRepository
}

// NewUserResource builds the resource with a Pop repository.
func NewUserResource(tx *pop.Connection) *UserResource {
	return &UserResource{repo: repositories.NewPopUserRepository(tx)}
}

// List handles GET /api/users
func (r *UserResource) List(c buffalo.Context) error {
	users, err := r.repo.FindAll()
	if err != nil {
		return c.Error(http.StatusInternalServerError, err)
	}
	return c.Render(http.StatusOK, render.JSON(users))
}

// Show handles GET /api/users/{user_id}
func (r *UserResource) Show(c buffalo.Context) error {
	u, err := r.repo.FindByID(c.Param("user_id"))
	if err != nil {
		return c.Error(http.StatusNotFound, err)
	}
	return c.Render(http.StatusOK, render.JSON(u))
}

// Create handles POST /api/users
func (r *UserResource) Create(c buffalo.Context) error {
	user := &models.User{}
	if err := c.Bind(user); err != nil {
		return c.Error(http.StatusBadRequest, err)
	}
	if err := r.repo.Create(user); err != nil {
		return c.Error(http.StatusUnprocessableEntity, err)
	}
	return c.Render(http.StatusCreated, render.JSON(user))
}

// Update handles PUT /api/users/{user_id}
func (r *UserResource) Update(c buffalo.Context) error {
	user, err := r.repo.FindByID(c.Param("user_id"))
	if err != nil {
		return c.Error(http.StatusNotFound, err)
	}
	if err := c.Bind(user); err != nil {
		return c.Error(http.StatusBadRequest, err)
	}
	if err := r.repo.Update(user); err != nil {
		return c.Error(http.StatusUnprocessableEntity, err)
	}
	return c.Render(http.StatusOK, render.JSON(user))
}

// Destroy handles DELETE /api/users/{user_id}
func (r *UserResource) Destroy(c buffalo.Context) error {
	user, err := r.repo.FindByID(c.Param("user_id"))
	if err != nil {
		return c.Error(http.StatusNotFound, err)
	}
	if err := r.repo.Delete(user); err != nil {
		return c.Error(http.StatusInternalServerError, err)
	}
	return c.Render(http.StatusNoContent, nil)
}
