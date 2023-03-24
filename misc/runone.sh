#!/bin/bash

# Check if the folder path was provided as a command line argument
if [ -z "$1" ]; then
  echo "Error: Please provide a folder path as a command line argument"
  exit 1
fi

# Remove the trailing / from the folder path (if present)
folder=${1%/}

# Check if the specified folder exists
if [ ! -d "$folder" ]; then
  echo "Error: $folder does not exist"
  exit 1
fi

# Iterate over the files in the folder
for file in "$folder"/*; do
  # Check if the file is a regular file (not a directory or symlink)
  if [ -f "$file" ]; then
          ./thesis-2022-regev-code/one.sh -b 90 $file
  fi
done
