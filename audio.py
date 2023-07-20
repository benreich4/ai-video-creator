from google.cloud import texttospeech
from util import path
import os

def gen(styleOf, topic, x):
  with open(f'{path(styleOf, topic)}/text/{x}.txt', 'r') as f:
    prompt = f.readlines()[0]
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=prompt)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB", 
        name="en-GB-Neural2-D"
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch= -3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )

    fn = f"{path(styleOf, topic)}/audio/{x}.mp3"
    # The response's audio_content is binary.
    with open(fn, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {fn}')
