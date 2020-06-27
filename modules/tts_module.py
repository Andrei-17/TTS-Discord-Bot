from gtts import gTTS
import boto3
import os

def googleTTS(text : str, path : str, language : str):
    audio = gTTS(text=text, lang=language)
    audio_path = "audio/{}.mp3".format(path)
    open(audio_path, "w")
    audio.save(audio_path)
    return audio_path

def polly(text : str, path : str, voiceId : str):
    polly = boto3.client(
        "polly",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    ttsResult = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voiceId)
    audio_path = "{}.mp3".format(path)
    charsNum = int(open("polly_chars.txt").read())
    charsNum += len(text)
    with open("polly_chars.txt", "w") as file:
        file.write(str(charsNum))
    with open(audio_path, "wb") as file:
        file.write(ttsResult["AudioStream"].read())
    return audio_path