package main

import (
	"fmt"
	"github.com/jozsefsallai/gophersauce"
	"saucenao/paths"
)

func scan(root string, sauce *gophersauce.Client) {
	err, images := paths.WalkRootDirectory(root)
	if err != nil {
		panic(err)
	}

	var matches map[string]paths.ImageFile
	matches = make(map[string]paths.ImageFile)

	doRateLimitedSaucenaoSearches(&images, sauce)

	for _, img := range images {
		match, ok := matches[img.Metadata.Header.IndexName]
		if ok {
			// Found duplicate.
			fmt.Printf("Duplicate found: %+v, %+v", match, img)
		}
	}
}
