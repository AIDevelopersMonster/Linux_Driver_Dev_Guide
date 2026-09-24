#!/usr/bin/env bash
set -euo pipefail

MODULE_NAME="garvis_greet"
MODULE_FILE="${MODULE_NAME}.ko"
BUILD_DIR="${KDIR:-/lib/modules/$(uname -r)/build}"

echo "Garvis kernel module demo"
echo "Kernel: $(uname -r)"
echo "Build directory: ${BUILD_DIR}"

if [[ ! -d "${BUILD_DIR}" ]]; then
    echo "ERROR: kernel build directory not found:"
    echo "  ${BUILD_DIR}"
    echo
    echo "Install matching kernel headers or run:"
    echo "  KDIR=/path/to/linux ./demo_garvis_greet.sh"
    exit 1
fi

if lsmod | grep -q "^${MODULE_NAME} "; then
    echo "Module is already loaded. Removing it first..."
    sudo rmmod "${MODULE_NAME}"
fi

echo "1. Cleaning previous build..."
make KDIR="${BUILD_DIR}" clean

echo "2. Building ${MODULE_FILE}..."
make KDIR="${BUILD_DIR}"

echo "3. Loading ${MODULE_FILE}..."
sudo insmod "${MODULE_FILE}"

echo "4. Recent kernel messages:"
echo "---------------------------------------------"
sudo dmesg | tail -n 10
echo "---------------------------------------------"

read -r -p "Press [Enter] to unload the module..."

sudo rmmod "${MODULE_NAME}"

echo "Module unloaded."
echo "Final kernel messages:"
sudo dmesg | tail -n 5
