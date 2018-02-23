#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

report_error(){
    notify-send "WhatAmIListeningTo" "ERROR: $1"
    exit 1
}

if [ ! -d "$DIR/.venv" ]; then
    report_error "Virtualenv not found. Run install.sh first."
fi

source "$DIR/.venv/bin/activate"

python "$DIR/run.py" & spotify
pkill -f "$DIR/run.py"