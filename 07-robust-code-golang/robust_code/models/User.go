package models

import (
	"encoding/json"
	"time"

	"github.com/gofrs/uuid"
	"github.com/gobuffalo/pop/v6"
	"github.com/gobuffalo/validate/v3"
	"github.com/gobuffalo/validate/v3/validators"
)

// User is used by Pop to map your users database table to your Go code.
type User struct {
	ID              uuid.UUID   `db:"id" json:"id"`
	Name            string      `db:"name" json:"name"`
	Email           string      `db:"email" json:"email"`
	EmailVerifiedAt *time.Time  `db:"email_verified_at" json:"email_verified_at,omitempty"`
	Password        string      `db:"password" json:"-"`
	RememberToken   *string     `db:"remember_token" json:"-"`
	CreatedAt       time.Time   `db:"created_at" json:"created_at"`
	UpdatedAt       time.Time   `db:"updated_at" json:"updated_at"`
}

// String is not required by Pop and may be deleted
func (u User) String() string {
	ju, _ := json.Marshal(u)
	return string(ju)
}

// Users is not required by Pop and may be deleted
type Users []User

// String is not required by Pop and may be deleted
func (u Users) String() string {
	ju, _ := json.Marshal(u)
	return string(ju)
}

// Validate gets run every time you call a "pop.Validate*" method.
// It ensures Name and Password are present.
func (u *User) Validate(tx *pop.Connection) (*validate.Errors, error) {
	return validate.Validate(
		&validators.StringIsPresent{Field: u.Name, Name: "name"},
		&validators.StringIsPresent{Field: u.Password, Name: "password"},
	), nil
}

// ValidateCreate gets run when you call "pop.ValidateAndCreate".
// Add creation-specific validations here.
func (u *User) ValidateCreate(tx *pop.Connection) (*validate.Errors, error) {
	return validate.NewErrors(), nil
}

// ValidateUpdate gets run when you call "pop.ValidateAndUpdate".
// Add update-specific validations here.
func (u *User) ValidateUpdate(tx *pop.Connection) (*validate.Errors, error) {
	return validate.NewErrors(), nil
}
