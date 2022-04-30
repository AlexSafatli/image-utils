package paths

import (
	"os"
	"path/filepath"
	"strings"
)

func WalkRootDirectory(root string) (err error, paths []ImageFile) {
	var cleanRoot = filepath.Clean(root)
	err = filepath.Walk(cleanRoot, func(path string, info os.FileInfo, err error) error {
		if err != nil || path == cleanRoot || strings.HasPrefix(info.Name(), ".") {
			return nil // ignore hidden files, etc.
		}
		if IsImageFile(info.Name()) {
			img := ImageFile{
				Path: path,
				Name: info.Name(),
				Size: float64(info.Size()),
			}
			paths = append(paths, img)
		} else if cleanRoot == filepath.Dir(path) {
			return nil
		}
		return nil
	})
	return
}
