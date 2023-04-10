package main

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"os"
	"path/filepath"
	"time"
)

const (
	totalSize       = 3 * 1024 * 1024 * 1024 // 3GB
	numFiles        = 2000
	avgSize         = 1024 * 1024 * 10
	duplicatePrefix = "duplicate"
	numDuplicates   = 500
)

var (
	extensions = []string{".avi", ".jpg", ".html", ".txt", ".xls", ".odt", ".doc", ".mp3", ".mp4", ".cad", ".exe", ".png"}
)

func main() {
	rand.Seed(time.Now().UnixNano())
	cwd, err := os.Getwd()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	testfolder := filepath.Join(cwd, "testfolder")

	err = os.MkdirAll(testfolder, 0755)
	if err != nil {
		fmt.Println("Error creating directory:", err)
		return
	}

	for i := 1; i <= numFiles; i++ {
		fileSize := int64(rand.Intn(avgSize))
		ext := extensions[rand.Intn(len(extensions))]
		filename := fmt.Sprintf("file%04d%s", i, ext)
		filedir := filepath.Join(testfolder, filename)
		err = createFile(filedir, fileSize)
		if err != nil {
			fmt.Println("Error creating file:", err)
			continue
		}
	}
	err = createDuplicates(testfolder)
	if err != nil {
		fmt.Println("Error creating duplicate file:", err)
	}

	fmt.Println("Files created successfully!")
}

func createFile(filepath string, size int64) error {
	f, err := os.Create(filepath)
	if err != nil {
		return err
	}
	defer f.Close()

	buf := make([]byte, 1024)
	for i := int64(0); i < size; i += 1024 {
		_, err := f.Write(buf)
		if err != nil {
			return err
		}
	}

	return nil
}
func createDuplicates(fileDir string) error {

	files, err := os.ReadDir(fileDir)
	if err != nil {
		return err
	}

	// Shuffle the files randomly
	rand.Seed(time.Now().UnixNano())
	rand.Shuffle(len(files), func(i, j int) {
		files[i], files[j] = files[j], files[i]
	})

	// Select the first numDuplicates files
	selectedFiles := files[:numDuplicates]

	// Create the duplicates
	for i, file := range selectedFiles {
		// Read the file contents
		fileData, err := ioutil.ReadFile(filepath.Join(fileDir, file.Name()))
		if err != nil {
			fmt.Printf("Error reading file %s: %s\n", file.Name(), err)
			return err
		}

		// Create the duplicate file
		duplicateName := fmt.Sprintf("%s%03d_%s", duplicatePrefix, i+1, file.Name())
		duplicatePath := filepath.Join(fileDir, duplicateName)
		duplicateFile, err := os.Create(duplicatePath)
		if err != nil {
			fmt.Printf("Error creating duplicate file %s: %s\n", duplicateName, err)
			return err
		}

		// Write the file contents to the duplicate file
		_, err = io.Copy(duplicateFile, bytes.NewReader(fileData))
		if err != nil {
			fmt.Printf("Error copying file contents to %s: %s\n", duplicateName, err)
			return err
		}

		// Close the duplicate file
		err = duplicateFile.Close()
		if err != nil {
			fmt.Printf("Error closing file %s: %s\n", duplicateName, err)
			return err
		}
	}
	return nil
}
