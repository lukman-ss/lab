package actions

import (
	"sync"

	"robust_code/locales"
	"robust_code/models"

	auth "robust_code/actions/api/authentication"
	userRes "robust_code/resource"

	"github.com/gobuffalo/buffalo"
	"github.com/gobuffalo/buffalo-pop/v3/pop/popmw"
	"github.com/gobuffalo/envy"
	"github.com/gobuffalo/middleware/i18n"
	"github.com/gobuffalo/middleware/paramlogger"
)

var (
	ENV     = envy.Get("GO_ENV", "development")
	app     *buffalo.App
	appOnce sync.Once
	T       *i18n.Translator
)

func App() *buffalo.App {
	appOnce.Do(func() {
		app = buffalo.New(buffalo.Options{
			Env:         ENV,
			SessionName: "_robust_code_session",
		})

		// Global DB transaction
		app.Use(popmw.Transaction(models.DB))

		// Log request params
		app.Use(paramlogger.ParameterLogger)

		// i18n (optional)
		app.Use(translations())

		// Authentication endpoints
		app.POST("/api/auth/register", auth.Register)
		app.POST("/api/auth/login",    auth.Login)
		app.POST("/api/auth/logout",   auth.Logout)

		// User CRUD Resource (no extra middleware here)
		app.Resource(
			"/api/users",
			userRes.NewUserResource(models.DB),
		)
	})

	return app
}

func translations() buffalo.MiddlewareFunc {
	var err error
	if T, err = i18n.New(locales.FS(), "en-US"); err != nil {
		app.Stop(err)
	}
	return T.Middleware()
}
