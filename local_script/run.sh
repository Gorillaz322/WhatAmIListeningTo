#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DEBUG=true

report_error(){
    notify-send "WhatAmIListeningTo" "ERROR: $1"
    exit 1
}

if [ ! -d "$DIR/.venv" ]; then
    report_error "Virtualenv not found. Run install.sh first."
fi

source "$DIR/.venv/bin/activate"

if [ "$DEBUG" = true ] ; then
    export API_URL="localhost:8000/"
    python "$DIR/run.py"
else
#    export API_URL="will be done soon"
    python "$DIR/run.py" & spotify
    pkill -f "$DIR/run.py"
fi