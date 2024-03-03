from pydub import AudioSegment
import math

# Load the audio file
audio = AudioSegment.from_wav("francine.wav")

# Define the length of each split in milliseconds
split_length = 60 * 1000

# Calculate the number of splits needed
num_splits = math.ceil(len(audio) / split_length)

# Split the audio and export
for i in range(num_splits):
    start = i * split_length
    end = min((i + 1) * split_length, len(audio))
    split_audio = audio[start:end]
    split_audio.export(f"francine_part{i+1}.wav", format="wav")

