package paths

import (
	"github.com/jozsefsallai/gophersauce"
	"path/filepath"
)

type ImageDirectory struct {
	Path         string   `json:"Path"`
	Name         string   `json:"Name"`
	Size         float64  `json:"Size"`
	NumberImages uint     `json:"Number of Images,omitempty"`
	ImagePaths   []string `json:"-"`
}

type ImageFile struct {
	Path     string  `json:"Path"`
	Name     string  `json:"Name"`
	Size     float64 `json:"Size"`
	Metadata *gophersauce.SearchResult
}

func IsImageFile(basename string) bool {
	var ext = filepath.Ext(basename)
	if len(ext) > 0 {
		ext = ext[1:] // trim the dot
	}
	return ext == "png" || ext == "jpg" || ext == "jpeg" || ext == "tiff" ||
		ext == "bmp" || ext == "webp"
}
