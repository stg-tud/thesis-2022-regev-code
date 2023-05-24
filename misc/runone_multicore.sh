#!/bin/bash

# Input Parameter for path containing settings files
if [ -z "$1" ]; then
  echo "Error: Please provide a path to the directory containing the setting files"
  exit 1
fi
folder=${1%/}

if [ ! -d "$folder" ]; then
  echo "Error: $folder does not exist"
  exit 1
fi

# Create temp folder for setting files
confdir=$(mktemp -d)
python3 thesis-2022-regev-code/misc/settings_generator.py --input "$1" --output "$confdir"

# Count of max processors
max_processes=4
running_processes=0

current_file=0
total_files=$(ls "$confdir" | wc -l)

for file in "$confdir"/*; do
  if [ -f "$file" ]; then
    for i in {0..3}; do
      if ! pgrep -a one.sh | grep -q numactl.*-C.*$i; then
        ((current_file++))
        echo "Started config $current_file/$total_files"
        # run the-one on specific core
        numactl --physcpubind=$i ./thesis-2022-regev-code/one.sh -b 1 "$file" &
        ((running_processes++))
        break
      fi
    done
    if [ "$running_processes" -eq "$max_processes" ]; then
      wait -n
      ((running_processes--))
    fi
  fi
done

wait

rm -rf "$confdir"
