#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

report_error(){
    echo "ERROR: $1"
    exit 1
}

if command -v spotify >/dev/null 2>&1 ; then
    echo "Spotify found"
else
    report_error "Spotify not found"
fi

if ! command -v playerctl >/dev/null 2>&1 ; then
    report_error "playerctl not found"
fi

if ! command -v virtualenv >/dev/null 2>&1 ; then
    report_error "virtualenv not found"
fi

VIRTUALENVDIR="$DIR/.venv"

virtualenv "$VIRTUALENVDIR"

source "$VIRTUALENVDIR/bin/activate"

if ! command -v pip >/dev/null 2>&1 ; then
    report_error "pip not found"
fi

pip install -r "$DIR/requirements.txt"

REPLACEMENT=".$DIR/run.sh"
sudo sed -i "s@Exec=spotify@Exec=$REPLACEMENT@g" /usr/share/applications/spotify.desktop