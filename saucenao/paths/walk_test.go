package paths

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
)

const tmpTreeRoot = "testing"

func prepareTestRoot() (string, error) {
	tmp, err := ioutil.TempDir("", tmpTreeRoot)
	if err != nil {
		return "", fmt.Errorf("Could not create temporary dir: %v\n", err)
	}
	return tmp, err
}

func prepareTestTree(tmp, tree string) (string, error) {
	var path = filepath.Join(tmp, tree)
	err := os.MkdirAll(path, 0755)
	if err != nil {
		_ = os.RemoveAll(path)
		return "", err
	}
	empty, err := os.Create(filepath.Join(path, "empty.jpeg"))
	if err != nil {
		_ = os.RemoveAll(path)
		return "", err
	}
	_ = empty.Close()
	return path, err
}

func TestWalkRootDirectory(t *testing.T) {
	tmp, err := prepareTestRoot()
	if err != nil {
		t.Error(err)
		return
	}

	tmpA, errA := prepareTestTree(tmp, "Internet Pictures/Oh My Goddess")
	tmpB, errB := prepareTestTree(tmp, "SFW/Art/Artist")
	if errA != nil {
		t.Error(errA)
	}
	if errB != nil {
		t.Error(errB)
	}
	defer os.RemoveAll(tmpA)
	defer os.RemoveAll(tmpB)

	err, paths := WalkRootDirectory(tmp)
	if err != nil {
		t.Error(err)
		return
	}
	if len(paths) != 2 {
		t.Errorf("Root: %s\nDid not find 2 paths, found %d instead\n%+v",
			os.TempDir(), len(paths), paths)
		return
	}
}
