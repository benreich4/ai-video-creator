from google.cloud import texttospeech_v1beta1 as tts
from util import path
from util import getLength
import os

def genSSML(parts):
    ssml = "<speak>"
    for i in range(0, len(parts)):
        ssml = ssml + parts[i]
        if i != len(parts) - 1:
            ssml = ssml + f' <mark name="{i}"/> '
    ssml = ssml + "</speak>"
    return ssml

def srtTime(rt):
    rts = str(int(rt // 1)).rjust(2,"0")
    rtms = str((rt % 1) + 0.0001)[2:5]
    return f"00:00:{rts},{rtms}"

def genSubs(styleOf, topic, x, parts, timepoints):
    p = f'{path(styleOf, topic)}/subtitles/{x}.srt'
    with open(p, 'w+') as f:
        lt = 0
        vlen=getLength(styleOf, topic, x)
        for k in range(0, len(parts)):
            f.write(str(k+1))
            f.write("\n")
            if k < len(parts)-1:
                rt = timepoints[k]
            else:
                rt = vlen
            f.write(srtTime(lt) + " --> " + srtTime(rt))
            lt = rt
            f.write("\n")
            f.write(parts[k])
            f.write("\n\n")
    print(f'Subtitles written to file {p}')


def gen(styleOf, topic, x):
  with open(f'{path(styleOf, topic)}/text/{x}.txt', 'r') as f:
    prompt = f.readlines()[0]
    # Instantiates a client
    client = tts.TextToSpeechClient()

    ws = prompt.split(" ")
    wss = [ws[i:i + 1] for i in range(0, len(ws), 1)] 
    parts = [" ".join(wss[i]) for i in range(0, len(wss))]
    ssmlPrompt = genSSML(parts)

    # Set the text input to be synthesized
    synthesis_input = tts.SynthesisInput(ssml=ssmlPrompt)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = tts.VoiceSelectionParams(
        language_code="en-GB", 
        name="en-GB-Neural2-D"
    )

    # voice = tts.VoiceSelectionParams(
    #     language_code="en-US", 
    #     name="en-US-Neural2-F"
    # )

    # Select the type of audio file you want returned
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        pitch= -3,
        speaking_rate = 1.25
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    request = tts.SynthesizeSpeechRequest(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config,
        enable_time_pointing=[ "SSML_MARK"]
    )

    response = client.synthesize_speech(request=request)
    response.timepoints.sort(key=lambda x: x.time_seconds)
    tps = list(map(lambda x: x.time_seconds, response.timepoints))

    fn = f"{path(styleOf, topic)}/audio/{x}.mp3"
    # The response's audio_content is binary.
    with open(fn, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {fn}')

    genSubs(styleOf, topic, x, parts, tps)
