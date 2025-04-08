#!/bin/bash

# Enable strict error handling
set -euo pipefail

# Function to convert absolute paths to project-relative paths
convert_to_relative_path() {
    local absolute_path=$1
    local project_dir=$2
    relative_path=${absolute_path#$project_dir/}  # Remove project_dir prefix
    echo "./${relative_path}"  # Return relative path with "./"
}

# Function to resolve absolute icon paths
resolve_icon_path() {
    local project_dir=$1
    local filename=$2
    echo "${project_dir}/media/media-ico/${filename}"  # Return absolute icon path
}

# Define project directory and verbosity
script_dir=$(dirname "$(realpath "$0")")
project_dir=$(realpath "${script_dir}/../../")  # Go up two levels to the project root
project_dir_name=$(basename "$project_dir")    # Extract project directory name

# Flags for verbosity
verbose=false
silent=false

# Parse flags
while [[ $# -gt 0 ]]; do
    case $1 in
        -Verbose)
            verbose=true
            ;;
        -Silent)
            silent=true
            ;;
        *)
            echo "Unknown flag: $1"
            exit 1
            ;;
    esac
    shift
done

# Find all desktop.ini files
desktop_ini_files=$(find "$project_dir" -type f -name "desktop.ini")

if [[ -z "$desktop_ini_files" ]]; then
    $verbose && echo "No desktop.ini files found."
    exit 0
fi

# Process each desktop.ini file
while IFS= read -r desktop_ini_path; do
    relative_desktop_ini_path=$(convert_to_relative_path "$desktop_ini_path" "$project_dir")
    
    # Read and process content
    if ! file_content=$(<"$desktop_ini_path"); then
        $verbose && echo "Failed to read: $relative_desktop_ini_path"
        continue
    fi

    updated_content=""
    changed=false
    current_icon_filename=""
    relative_icon_path=""
    absolute_icon_path=""

    # Process each line
    while IFS= read -r line; do
        if [[ "$line" == IconResource=* ]]; then
            existing_filename=$(basename "${line#IconResource=}")
            current_icon_filename=$existing_filename
            absolute_icon_path=$(resolve_icon_path "$project_dir" "$existing_filename")
            relative_icon_path=$(convert_to_relative_path "$absolute_icon_path" "$project_dir")

            if [[ "$line" != "IconResource=${absolute_icon_path}" ]]; then
                updated_content+="IconResource=${absolute_icon_path}"$'\n'
                changed=true
            else
                updated_content+="$line"$'\n'
            fi
        else
            updated_content+="$line"$'\n'
        fi
    done <<< "$file_content"

    # Write changes if any
    if $changed; then
        echo "$updated_content" > "$desktop_ini_path"
        $verbose && echo "$relative_desktop_ini_path -> $relative_icon_path"
    else
        $verbose && echo "$relative_desktop_ini_path ~ $relative_icon_path"
    fi

done <<< "$desktop_ini_files"

exit 0