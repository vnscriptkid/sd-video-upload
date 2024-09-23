package main

import (
	"fmt"
	"net/http"
)

func main() {
	// Serve static files like video and html files from the "static" folder
	fs := http.FileServer(http.Dir("./static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	// Serve the main HTML page
	http.HandleFunc("/", serveHTML)

	// Start the server on port 8080
	fmt.Println("Server started at http://localhost:8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error starting server:", err)
	}
}

// serveHTML serves the HTML file
func serveHTML(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "./static/index.html")
}
