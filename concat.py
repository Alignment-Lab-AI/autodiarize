from pydub import AudioSegment

# Load the audio files
audio1 = AudioSegment.from_wav('francine1.wav')
audio2 = AudioSegment.from_wav('francine2.wav')

# Concatenate the audio files
combined_audio = audio1 + audio2

# Export the concatenated audio to a new file
combined_audio.export("francine_combined.wav", format="wav")
