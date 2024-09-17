#!/bin/zsh

# Check if a directory is provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/directory"
  exit 1
fi

# Get the directory from the argument
DIRECTORY="$1"

# Verify that the given argument is a directory
if [ ! -d "$DIRECTORY" ]; then
  echo "Error: $DIRECTORY is not a directory."
  exit 1
fi

# Create an output directory if needed (optional)
OUTPUT_DIR="${DIRECTORY}/converted_mp3"
mkdir -p "$OUTPUT_DIR"

# Find all .m4a files in the directory and its subdirectories
find "$DIRECTORY" -type f -name '*.m4a' | while IFS= read -r FILE; do
  # Define the output file name
  RELATIVE_PATH="${FILE#$DIRECTORY/}"
  OUTPUT="${OUTPUT_DIR}/${RELATIVE_PATH%.m4a}.mp3"

  # Ensure the output directory exists
  OUTPUT_DIR_PATH="$(dirname "$OUTPUT")"
  mkdir -p "$OUTPUT_DIR_PATH"

  # Perform the conversion
  ffmpeg -i -nostdin "$FILE" "$OUTPUT" 2>> conversion_errors.log

  # Check if the conversion was successful
  if [ $? -eq 0 ]; then
    echo "Converted $FILE to $OUTPUT"
  else
    echo "Failed to convert $FILE" >> conversion_errors.log
  fi
done
one