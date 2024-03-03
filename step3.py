import pysrt
import os
from pydub import AudioSegment

# Function to ensure directory exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Load the SRT file
subs = pysrt.open('audio.srt')

# Load the WAV file
audio = AudioSegment.from_wav('audio.wav')

# Base directory for the LJ Speech-like structure
base_dir = "LJ_Speech_dataset"

# Dictionary to hold audio segments and texts for each speaker
speaker_audios_texts = {}

# Process each subtitle
for sub in subs:
    start_time = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
    end_time = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
    
    # Extract speaker and text from the subtitle
    speaker_text = sub.text.split(':')
    if len(speaker_text) > 1:
        speaker = speaker_text[0].strip()
        text = ':'.join(speaker_text[1:]).strip()
        segment = audio[start_time:end_time]
        
        # Append or create the audio segment and text for the speaker
        if speaker not in speaker_audios_texts:
            speaker_audios_texts[speaker] = []
        speaker_audios_texts[speaker].append((segment, text))

# Save each speaker's audio to a separate file and generate metadata
for speaker, segments_texts in speaker_audios_texts.items():
    speaker_dir = os.path.join(base_dir, speaker.replace(' ', '_'))
    ensure_dir(speaker_dir)
    
    metadata_lines = []
    for i, (segment, text) in enumerate(segments_texts, start=1):
        filename = f"{speaker.replace(' ', '_')}_{i:03}.wav"
        filepath = os.path.join(speaker_dir, filename)
        segment.export(filepath, format="wav")
        
        # Prepare metadata line (filename without extension, text)
        metadata_lines.append(f"{filename[:-4]}|{text}|{text}")
    
    # Save metadata to a file
    metadata_file = os.path.join(speaker_dir, "metadata.csv")
    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write("\n".join(metadata_lines))
    
    print(f"Exported files and metadata for {speaker}")
