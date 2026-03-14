#!/bin/bash
"""Synchronize the current directory to the CIRCUITPY drive, excluding .git and this deploy script."""
DESTINO="/media/$USER/CIRCUITPY/"

rsync -av --exclude='.git' --exclude='deploy.sh' ./ "$DESTINO"
sync