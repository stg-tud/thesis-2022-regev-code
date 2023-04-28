#!/bin/bash

# Check if the folder path was provided as a command line argument
if [ -z "$1" ]; then
  echo "Error: Please provide a folder path as a command line argument"
  exit 1
fi


if [ -z "$2" ]; then
  echo "Error: Please provide the number of runs parameter"
  exit 1
fi

# Remove the trailing / from the folder path (if present)
folder=${1%/}

# Check if the specified folder exists
if [ ! -d "$folder" ]; then
  echo "Error: $folder does not exist"
  exit 1
fi

# Set the maximum number of background processes to run at once
max_processes=4
# Initialize the counter for running background processes to 0
running_processes=0

# Iterate over the files in the folder
for file in "$folder"/*; do
  # Check if the file is a regular file (not a directory or symlink)
  if [ -f "$file" ]; then
    # Find a free CPU core to use
    for i in {0..3}; do
      if ! pgrep -a one.sh | grep -q numactl.*-C.*$i; then
        # Bind the process to the CPU using numactl, and launch the process in the background
        numactl --physcpubind=$i ./thesis-2022-regev-code/one.sh -b $2 "$file" &
        ((running_processes++))
        break
      fi
    done
    # If the maximum number of processes is running, wait for one to finish before starting another
    if [ "$running_processes" -eq "$max_processes" ]; then
      wait -n
      ((running_processes--))
    fi
  fi
done

# Wait for all remaining background processes to finish
wait
