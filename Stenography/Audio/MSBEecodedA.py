import wave

def encode_msb_audio(input_audio_path, output_audio_path, secret_message):
    # Open the audio file
    audio = wave.open(input_audio_path, mode='rb')
    frames = audio.readframes(audio.getnframes())
    samples = list(frames)
    audio.close()

    # Convert the secret message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)

    # Embed the binary message into the most significant bit of the audio samples
    for i, bit in enumerate(binary_message):
        samples[i] = (samples[i] & 0x7F) | (int(bit) << 7)

    # Write the modified audio samples to a new audio file
    with wave.open(output_audio_path, 'wb') as output_audio:
        output_audio.setparams(audio.getparams())
        output_audio.writeframes(bytes(samples))

# Example usage
encode_msb_audio("input_audio.wav", "encoded_audio_msb.wav", "Secret message")
