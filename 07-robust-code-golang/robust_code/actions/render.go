package actions

import "github.com/gobuffalo/buffalo/render"

var r *render.Engine

func init() {
	// API-only: no HTML templates or assets needed.
	r = render.New(render.Options{})
}
	