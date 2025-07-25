package grifts

import (
	"robust_code/actions"

	"github.com/gobuffalo/buffalo"
)

func init() {
	buffalo.Grifts(actions.App())
}
