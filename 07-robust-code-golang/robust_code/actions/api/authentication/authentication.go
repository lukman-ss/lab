package authentication

import (
	"net/http"

	"github.com/gobuffalo/buffalo"
	"github.com/gobuffalo/buffalo/render"
	"github.com/gobuffalo/pop/v6"

	"robust_code/requests"
	authsvc "robust_code/services"
)

// Register handles POST /api/auth/register
func Register(c buffalo.Context) error {
	tx := c.Value("tx").(*pop.Connection)

	var req requests.AuthenticationRequest
	if err := c.Bind(&req); err != nil {
		return c.Error(http.StatusBadRequest, err)
	}
	if verrs := req.ValidateRegister(); verrs.HasAny() {
		return c.Render(http.StatusUnprocessableEntity, render.JSON(verrs))
	}

	svc := authsvc.NewAuthenticationService(tx)
	user, err := svc.Register(req.Name, req.Email, req.Password)
	if err != nil {
		if err.Error() == "email already in use" {
			return c.Render(http.StatusConflict, render.JSON(map[string]string{"email": err.Error()}))
		}
		return c.Error(http.StatusInternalServerError, err)
	}
	return c.Render(http.StatusCreated, render.JSON(user))
}

// Login handles POST /api/auth/login
func Login(c buffalo.Context) error {
	tx := c.Value("tx").(*pop.Connection)

	var req requests.AuthenticationRequest
	if err := c.Bind(&req); err != nil {
		return c.Error(http.StatusBadRequest, err)
	}
	if verrs := req.ValidateLogin(); verrs.HasAny() {
		return c.Render(http.StatusUnprocessableEntity, render.JSON(verrs))
	}

	svc := authsvc.NewAuthenticationService(tx)
	user, err := svc.Login(req.Email, req.Password)
	if err != nil {
		return c.Render(http.StatusUnauthorized, render.JSON(map[string]string{"error": err.Error()}))
	}
	return c.Render(http.StatusOK, render.JSON(user))
}

// Logout handles POST /api/auth/logout
func Logout(c buffalo.Context) error {
	tx := c.Value("tx").(*pop.Connection)

	var req requests.AuthenticationRequest
	if err := c.Bind(&req); err != nil {
		return c.Error(http.StatusBadRequest, err)
	}
	if verrs := req.ValidateLogout(); verrs.HasAny() {
		return c.Render(http.StatusUnprocessableEntity, render.JSON(verrs))
	}

	svc := authsvc.NewAuthenticationService(tx)
	if err := svc.Logout(req.Token); err != nil {
		return c.Error(http.StatusInternalServerError, err)
	}
	return c.Render(http.StatusOK, render.JSON(map[string]string{"message": "logged out"}))
}
