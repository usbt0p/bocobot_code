#!/bin/bash
"""Sincroniza el proyecto local con la unidad CIRCUITPY."""
DESTINO="/media/$USER/CIRCUITPY/" # Ajusta esta ruta según tu distro

rsync -av --exclude='.git' --exclude='deploy.sh' ./ "$DESTINO"
sync