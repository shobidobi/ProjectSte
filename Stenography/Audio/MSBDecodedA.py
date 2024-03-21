import wave


def decode_msb_audio(encoded_audio_path):
    # Open the encoded audio file
    audio = wave.open(encoded_audio_path, mode='rb')
    frames = audio.readframes(audio.getnframes())
    samples = list(frames)
    audio.close()

    # Extract the MSBs from the audio samples to reconstruct the binary message
    binary_message = ''
    for sample in samples:
        binary_message += str(sample >> 7)

    # Convert the binary message to ASCII characters
    decoded_message = ''.join([chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)])

    return decoded_message


# Example usage
decoded_message = decode_msb_audio("encoded_audio_msb.wav")
print("Decoded message:", decoded_message)
