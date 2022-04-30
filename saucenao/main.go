package main

import (
	"fmt"
	"github.com/jozsefsallai/gophersauce"
	"os"
)

func main() {
	// Check if arg length correct
	if len(os.Args) < 2 || len(os.Args) > 3 {
		fmt.Printf("Usage of %s:\n <root_path> [scan/clean]\n",
			os.Args[0])
		os.Exit(2)
	}

	// Read config files
	conf := loadConfigs()
	if conf.ApiKey == "" {
		panic("Need a SauceNao API key")
	}

	// Get path arguments
	var root = os.Args[1]
	var cmd = os.Args[2]

	// Connect to SauceNao
	sauce, err := gophersauce.NewClient(&gophersauce.Settings{APIKey: conf.ApiKey})
	if err != nil {
		panic(err)
	}

	// Perform whatever command was requested; this format is more or less
	// copied from the Senketsu main code routine.
	switch cmd {
	case "scan":
		scan(root, sauce)
		break
	case "clean":
		break
	default:
		_, _ = fmt.Fprintf(os.Stderr, "Command '%s' not supported", cmd)
		os.Exit(1)
	}
}
