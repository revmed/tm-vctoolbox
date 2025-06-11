#!/bin/bash
echo "Installing system dependencies for R packages via Homebrew..."

# Check if homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "Homebrew is not installed. Install it then rerun this script."
    exit 1
fi

brew update

# install common R build dependencies
brew install \
    pkg-config \
    freetype \
    harfbuzz \
    fribidi \
    libtiff \
    libjpeg \
    cairo \
    glib \
    fontconfig \
    cmake \
    pandoc \
    librsvg \
    python \
    homebrew/cask/basictex
    
eval "$(/usr/libexec/path_helper)"

echo "All required system libraries have been installed."
echo "If there are still compile errors, try restarting R or terminal."