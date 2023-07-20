from google.cloud import texttospeech_v1beta1
from util import path
import os

def gen(styleOf, topic, x):
  with open(f'{path(styleOf, topic)}/text/{x}.txt', 'r') as f:
    #prompt = f.readlines()[0]
prompt = "<speak><prosody><mark name=\"0\"/>I <mark name=\"1\"/>am <mark name=\"2\"/>my <mark name=\"3\"/>aunt's <mark name=\"4\"/>sister's <mark name=\"5\"/>daughter. <mark name=\"6\"/>He <mark name=\"7\"/>was <mark name=\"8\"/>sure <mark name=\"9\"/>the <mark name=\"10\"/>Devil <mark name=\"11\"/>created <mark name=\"12\"/>red <mark name=\"13\"/>sparkly <mark name=\"14\"/>glitter.</prosody></speak>"# Instantiates a client
client = texttospeech_v1beta1.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech_v1beta1.SynthesisInput(ssml=prompt)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech_v1beta1.VoiceSelectionParams(
    language_code="en-US", 
    name="en-US-Standard-A"
)

# Select the type of audio file you want returned
audio_config = texttospeech_v1beta1.AudioConfig(
    audio_encoding=texttospeech_v1beta1.AudioEncoding.MP3
    # pitch= -3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
request = texttospeech_v1beta1.SynthesizeSpeechRequest(
    input=synthesis_input, 
    voice=voice, 
    audio_config=audio_config,
    enable_time_pointing=[ "SSML_MARK"]
)

reponse = client.synthesize_speech(request=request)

    fn = f"{path(styleOf, topic)}/audio/{x}.mp3"
    # The response's audio_content is binary.
    with open(fn, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {fn}')
