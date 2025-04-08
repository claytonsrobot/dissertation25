#!/bin/bash

# Example usage:
# ./update_desktop_ini.sh --verbose --relative-ico-path "media/icons/"
# Parse input arguments
VERBOSE=false
RELATIVE_ICO_PATH=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --verbose) VERBOSE=true ;;  # Enable verbose logging
        --silent) VERBOSE=false ;;  # Suppress all logs
        --relative-ico-path) RELATIVE_ICO_PATH="$2"; shift ;;  # Capture relative icon path
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Set default relative path if not provided
if [[ -z "$RELATIVE_ICO_PATH" ]]; then
    RELATIVE_ICO_PATH="media/media-ico/"  # Default value
fi

# Echo debugging info if verbose is enabled
if $VERBOSE; then
    echo "RelativeIcoPath: $RELATIVE_ICO_PATH"
fi

# Determine project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"  # Go two levels up
PROJECT_DIR_NAME="$(basename "$PROJECT_DIR")"

# Function to convert absolute paths to project-relative paths
convert_to_relative_path() {
    local absolute_path=$1
    echo "./$PROJECT_DIR_NAME/${absolute_path#$PROJECT_DIR/}"
}

# Function to resolve absolute icon paths
resolve_icon_path() {
    local filename=$1
    echo "$PROJECT_DIR/$RELATIVE_ICO_PATH$filename"
}

# Find all desktop.ini files
DESKTOP_INI_FILES=$(find "$PROJECT_DIR" -name "desktop.ini" -type f)

if [[ -z "$DESKTOP_INI_FILES" ]]; then
    if $VERBOSE; then
        echo "No desktop.ini files found."
    fi
    exit 0
fi

# Iterate over each desktop.ini file
while IFS= read -r desktop_ini; do
    relative_desktop_ini_path=$(convert_to_relative_path "$desktop_ini")

    # Read and update desktop.ini content
    if [[ -f "$desktop_ini" ]]; then
        changed=false
        updated_lines=()
        while IFS= read -r line; do
            if [[ "$line" == IconResource=* ]]; then
                existing_filename=$(basename "${line#IconResource=}")
                absolute_icon_path=$(resolve_icon_path "$existing_filename")
                relative_icon_path=$(convert_to_relative_path "$absolute_icon_path")

                if $VERBOSE; then
                    echo "AbsoluteIconPath: $absolute_icon_path"
                    echo "RelativeIconPath: $relative_icon_path"
                fi

                if [[ "$line" != "IconResource=$absolute_icon_path" ]]; then
                    updated_lines+=("IconResource=$absolute_icon_path")
                    changed=true
                else
                    updated_lines+=("$line")
                fi
            else
                updated_lines+=("$line")
            fi
        done < "$desktop_ini"

        # Write changes back to desktop.ini if any
        if $changed; then
            printf "%s\n" "${updated_lines[@]}" > "$desktop_ini"
            if $VERBOSE; then
                echo "$relative_desktop_ini_path -> $relative_icon_path"
            fi
        else
            if $VERBOSE; then
                echo "$relative_desktop_ini_path ~ $relative_icon_path"
            fi
        fi
    fi
done <<< "$DESKTOP_INI_FILES"