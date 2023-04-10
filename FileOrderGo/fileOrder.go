package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"github.com/cespare/xxhash/v2"
)

// FileInfo represents information about a file
type FileInfo struct {
	path     string    // path to file
	size     int64     // file size in bytes
	hash     uint64    // file hash value
	ext      string    // file extension
	hasExt   bool      // true if file has extension, false otherwise
	isDup    bool      // true if file is a duplicate, false otherwise
	original *FileInfo // pointer to original file if this file is a duplicate, nil otherwise
}

// calculateHash calculates the hash value of a file using XXHash
func calculateHash(filePath string) (uint64, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return 0, err
	}
	defer file.Close()

	hasher := xxhash.New()
	_, err = io.Copy(hasher, file)
	if err != nil {
		return 0, err
	}

	return hasher.Sum64(), nil
}

// getFileInfo returns a FileInfo object for the given file path
func getFileInfo(filePath string) (*FileInfo, error) {
	info, err := os.Stat(filePath)
	if err != nil {
		return nil, err
	}

	hash, err := calculateHash(filePath)
	if err != nil {
		return nil, err
	}

	return &FileInfo{
		path:  filePath,
		size:  info.Size(),
		hash:  hash,
		isDup: false,
	}, nil
}

// removeDuplicates removes duplicate files in the given directory
func removeDuplicates(dirPath string) error {
	fileMap := make(map[int64]map[uint64]*FileInfo)
	var duplicates []*FileInfo

	err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Skip directories
		if info.IsDir() {
			return nil
		}

		fileInfo, err := getFileInfo(path)
		if err != nil {
			return err
		}

		// Check for duplicates
		if _, ok := fileMap[fileInfo.size]; !ok {
			fileMap[fileInfo.size] = make(map[uint64]*FileInfo)
		}
		if existingFile, ok := fileMap[fileInfo.size][fileInfo.hash]; ok {
			fileInfo.isDup = true
			fileInfo.original = existingFile
			duplicates = append(duplicates, fileInfo)
		} else {
			fileMap[fileInfo.size][fileInfo.hash] = fileInfo
		}

		return nil
	})
	if err != nil {
		return err
	}

	// Delete duplicate files
	for _, fileInfo := range duplicates {
		if fileInfo.original != nil {
			fmt.Printf("Deleting duplicate file: %s\n", fileInfo.path)
			err = os.Remove(fileInfo.path)
			if err != nil {
				return err
			}
		}
	}
	return nil
}

func organizeFilesByExtension(rootPath string) error {
	// Create a map to hold all the file extensions as keys
	// and their corresponding paths as values
	extMap := make(map[string]string)

	// Walk through the root directory and its subdirectories
	err := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Check if the current path is a regular file
		if !info.Mode().IsRegular() {
			return nil
		}

		// Get the file extension
		ext := filepath.Ext(info.Name())
		if ext == "" {
			return nil
		}

		// Get the full path of the extension folder
		extPath, ok := extMap[ext]
		if !ok {
			extPath = filepath.Join(rootPath, ext[1:])
			if err := os.Mkdir(extPath, 0755); err != nil {
				return err
			}
			extMap[ext] = extPath
		}

		// Move the file to the extension folder
		newPath := filepath.Join(extPath, info.Name())
		if err := os.Rename(path, newPath); err != nil {
			return err
		}

		return nil
	})

	return err
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Print("Enter directory")
	scanner.Scan()
	dirPath := scanner.Text()
	err := removeDuplicates(dirPath)
	if err != nil {
		fmt.Printf("Error removing duplicates: %s\n", err.Error())
		return
	}

	fmt.Println("Duplicate files removed successfully!")
	err = organizeFilesByExtension(dirPath)
	if err != nil {
		fmt.Printf("Error ordering file by extention: %s\n", err.Error())
		return
	}
}
