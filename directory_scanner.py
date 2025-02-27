import os

# Supported media formats
MEDIA_EXTENSIONS = {".mp3", ".wav", ".mp4", ".mkv", ".mov", ".flv", ".aac", ".m4a"}

def find_media_files(directory):
    """Recursively finds all media files in the directory."""
    media_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in MEDIA_EXTENSIONS):
                media_files.append(os.path.join(root, file))
    return media_files

# Example Usage
directory = r"C:\\media"  # Change this to your actual media directory
files = find_media_files(directory)
print(f"Found {len(files)} media files: {files}\n")
if not os.path.exists(directory):
    print(f"Directory {directory} does not exist.")
    exit()
