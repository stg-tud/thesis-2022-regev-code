#!/bin/sh

if [ "$(uname)" != "Linux" ]; then
    SCRIPT_DIR=$(dirname $(perl -MCwd -e 'print Cwd::abs_path shift' "$0"))
else
    SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
fi

echo "Starting the ONE from $SCRIPT_DIR"
java -Xmx1024M -cp $SCRIPT_DIR/target:$SCRIPT_DIR/lib/ECLA.jar:$SCRIPT_DIR/lib/DTNConsoleConnection.jar:$SCRIPT_DIR core.DTNSim $*
