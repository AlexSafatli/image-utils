package main

import (
	"fmt"
	"github.com/jozsefsallai/gophersauce"
	"saucenao/paths"
	"time"
)

const (
	maxNumSauceNaoRequestsPer30Seconds = 6
)

func makeLimiter() chan time.Time {
	limiter := make(chan time.Time, maxNumSauceNaoRequestsPer30Seconds)
	for i := 0; i < maxNumSauceNaoRequestsPer30Seconds; i++ {
		limiter <- time.Now()
	}
	go func() {
		for t := range time.Tick(30 * time.Second) {
			limiter <- t
		}
	}()
	return limiter
}

func doRateLimitedSaucenaoSearches(images *[]paths.ImageFile, sauce *gophersauce.Client) {
	limiter := makeLimiter()

	for _, img := range *images {
		<-limiter
		err := getSaucenaoMetadata(&img, sauce)
		if err != nil {
			fmt.Println(err)
		}
	}

	close(limiter)
}

func getSaucenaoMetadata(img *paths.ImageFile, sauce *gophersauce.Client) error {
	r, err := sauce.FromFile(img.Path)
	if err != nil {
		return err
	}
	match := r.First()
	img.Metadata = &match
	return nil
}
