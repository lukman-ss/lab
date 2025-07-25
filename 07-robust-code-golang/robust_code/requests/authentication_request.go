package requests

import (
	"github.com/gobuffalo/validate/v3"
	"github.com/gobuffalo/validate/v3/validators"
)

// AuthenticationRequest holds the JSON payload for auth endpoints.
type AuthenticationRequest struct {
	Name     string `json:"name,omitempty"`
	Email    string `json:"email"`
	Password string `json:"password,omitempty"`
	Token    string `json:"token,omitempty"`
}

// ValidateRegister ensures name, email, and password meet requirements.
func (r *AuthenticationRequest) ValidateRegister() *validate.Errors {
	return validate.Validate(
		&validators.StringIsPresent{Field: r.Name, Name: "name"},
		&validators.EmailIsPresent{Field: r.Email, Name: "email"},
		&validators.StringLengthInRange{Field: r.Password, Name: "password", Min: 6, Max: 100},
	)
}

// ValidateLogin ensures email and password are present.
func (r *AuthenticationRequest) ValidateLogin() *validate.Errors {
	return validate.Validate(
		&validators.EmailIsPresent{Field: r.Email, Name: "email"},
		&validators.StringIsPresent{Field: r.Password, Name: "password"},
	)
}

// ValidateLogout ensures a token is present.
func (r *AuthenticationRequest) ValidateLogout() *validate.Errors {
	return validate.Validate(
		&validators.StringIsPresent{Field: r.Token, Name: "token"},
	)
}
