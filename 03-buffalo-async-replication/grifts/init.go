package grifts

import (
	"03-buffalo-async-replication/actions"

	"github.com/gobuffalo/buffalo"
)

func init() {
	buffalo.Grifts(actions.App())
}
