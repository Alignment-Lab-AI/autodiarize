import pysrt
import os
from pydub import AudioSegment

# Load the SRT file
subs = pysrt.open('francine.srt')

# Load the WAV file
audio = AudioSegment.from_wav('francine.wav')

# Dictionary to hold audio segments for each speaker
speaker_audios = {}

# Process each subtitle
for sub in subs:
    start_time = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
    end_time = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
    
    # Extract speaker from the subtitle text
    speaker_text = sub.text.split(':')
    if len(speaker_text) > 1:
        speaker = speaker_text[0].strip()
        segment = audio[start_time:end_time]
        
        # Append or create the audio segment for the speaker
        if speaker in speaker_audios:
            speaker_audios[speaker] += segment
        else:
            speaker_audios[speaker] = segment

# Save each speaker's audio to a separate file
for speaker, audio_segment in speaker_audios.items():
    filename = f"{speaker.replace(' ', '_')}.wav"
    audio_segment.export(filename, format="wav")
    print(f"Exported {filename}")

