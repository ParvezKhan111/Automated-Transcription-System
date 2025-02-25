import whisper
from directory_scanner import find_media_files  # Import media scanning function

# Define the correct media directory
directory = r"C:\media"  # Use raw string (r"...") to avoid escape issues

# Scan for media files
files = find_media_files(directory)

def transcribe_audio(file_path):
    """Transcribes audio using the Whisper model and saves the text."""
    model = whisper.load_model("base")  # You can use "tiny", "small", "medium", or "large"
    result = model.transcribe(file_path)
    
    # Save transcription
    transcript_file = file_path + ".txt"
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Transcription saved: {transcript_file}")

# Debugging: Print found files
print(f"Found {len(files)} media files: {files}")

# Make sure we found files before transcribing
if files and len(files) > 0:
    transcribe_audio(files[0])  # Transcribe the first media file
else:
    print("No media files found. Make sure the media folder has audio files.")
