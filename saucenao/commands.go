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
	for _, img := range images {
		hash, err := getSaucenaoMetadata(&img, sauce)
		if err != nil {
			fmt.Println(err)
		}
		match, ok := matches[hash]
		if ok {
			// Found duplicate.
			//resolveDuplicate()
			fmt.Printf("Found duplicates: %+v, %+v", img, match)
		}
	}
}

func getSaucenaoMetadata(img *paths.ImageFile, sauce *gophersauce.Client) (hash string, err error) {
	r, err := sauce.FromFile(img.Path)
	if err != nil {
		return
	}
	match := r.First()
	hash = match.Header.IndexName
	img.Metadata = &match
	return
}
