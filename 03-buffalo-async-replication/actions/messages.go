package actions

import (
	"net/http"

	"github.com/gobuffalo/buffalo"
)

// MessagesIndex default implementation.
func MessagesIndex(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("messages/index.html"))
}


// MessagesCreate default implementation.
func MessagesCreate(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("messages/create.html"))
}


// MessagesShow default implementation.
func MessagesShow(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("messages/show.html"))
}


// MessagesDelete default implementation.
func MessagesDelete(c buffalo.Context) error {
	return c.Render(http.StatusOK, r.HTML("messages/delete.html"))
}

