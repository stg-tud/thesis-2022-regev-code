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

function ProgressBar {
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

printf "\rProgress : [${_fill// /#}${_empty// /-}] ${_progress}%%\n"

}


# Create temp folder for setting files
confdir=$(mktemp -d)
python3 thesis-2022-regev-code/misc/settings_generator.py --input "$1" --output "$confdir"

# Count of max processors
max_processes=8
running_processes=0

current_file=0
total_files=$(ls "$confdir" | wc -l)

for file in "$confdir"/*; do
  if [ -f "$file" ]; then
    for i in {0..7}; do
      if ! pgrep -a one.sh | grep -q numactl.*-C.*$i; then
        ((current_file++))
        echo "Started config $current_file/$total_files"
        ProgressBar ${current_file} ${total_files}
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
