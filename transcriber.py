import os
import time
import whisper
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Supported media file formats
SUPPORTED_MEDIA_EXTENSIONS = {".mp3", ".wav", ".mp4", ".mkv", ".mov", ".flv", ".aac", ".m4a"}

# Path to the log file for processed media files
PROCESSED_FILES_LOG = "processed_files.txt"

# Global media folder path
MEDIA_FOLDER_PATH = r"C:\media"

def get_processed_files():
    """Load the set of media file paths that have already been transcribed."""
    if os.path.exists(PROCESSED_FILES_LOG):
        with open(PROCESSED_FILES_LOG, "r") as log_file:
            return set(line.strip() for line in log_file if line.strip())
    return set()

def record_processed_file(file_path):
    """Record a media file as processed by appending its path to the log."""
    with open(PROCESSED_FILES_LOG, "a") as log_file:
        log_file.write(file_path + "\n")

def transcribe_media_file(file_path):
    """Transcribe a media file if it hasn't been processed yet,
    and save the transcript in the same folder as the media file."""
    processed_files = get_processed_files()
    if file_path in processed_files:
        print(f"⚠️ Skipping already processed file: {file_path}")
        return

    print(f"Transcribing file: {file_path}")
    model = whisper.load_model("base")  # Adjust model size as needed
    result = model.transcribe(file_path)

    # Save the transcript in the same folder as the media file
    transcript_path = os.path.join(os.path.dirname(file_path), os.path.basename(file_path) + ".txt")
    with open(transcript_path, "w", encoding="utf-8") as transcript_file:
        transcript_file.write(result["text"])

    print(f"✅ Transcription saved: {transcript_path}")
    record_processed_file(file_path)

class MediaFileEventHandler(FileSystemEventHandler):
    """Event handler for new media files."""
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        if any(file_path.lower().endswith(ext) for ext in SUPPORTED_MEDIA_EXTENSIONS):
            print(f"📂 New media file detected: {file_path}")
            transcribe_media_file(file_path)
            # Reprint the watching message after processing the file
            print(f"👀 Watching {MEDIA_FOLDER_PATH} for new media files...")

def perform_initial_transcription(root_directory):
    """Recursively scan the directory and transcribe all unprocessed media files."""
    for current_root, _, files in os.walk(root_directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in SUPPORTED_MEDIA_EXTENSIONS):
                full_file_path = os.path.join(current_root, file)
                transcribe_media_file(full_file_path)
    print("Initial transcription complete. Now watching for new media files...")

def monitor_directory(root_directory):
    """Start real-time monitoring of the directory (and subdirectories) for new media files."""
    observer = Observer()
    observer.schedule(MediaFileEventHandler(), root_directory, recursive=True)
    observer.start()
    print(f"👀 Watching {root_directory} for new media files...")
    try:
        while True:
            time.sleep(5)  # Keeps the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    print("Starting initial transcription of existing files...")
    perform_initial_transcription(MEDIA_FOLDER_PATH)
    monitor_directory(MEDIA_FOLDER_PATH)
