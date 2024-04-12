from google.cloud import speech, translate_v2 as translate, texttospeech
from google.cloud import storage
from pydub import AudioSegment
from scipy.io import wavfile
import io
import time
import subprocess
import ffmpeg
import whisper

# Initialize the GCP client for each service
speech_client = speech.SpeechClient()
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

# Load your video file and extract the audio
def convertVideoToMp3(input_file,output_file):
    ffmpeg_cmd = ["ffmpeg","-i",input_file,"-vn","-acodec","libmp3lame","-ab","192k","-ar","44100","-y",output_file]   
    # ffmpeg -i
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Successfully Converted")
    except subprocess.CalledProcessError as e:
        print("Conversion error")
convertVideoToMp3('input_video3.mp4','temp_audio.wav')


# Load the audio file
audio = whisper.load_audio("temp_audio.wav")

# Load the model
model = whisper.load_model("tiny")

print("Whisper - Model loaded Succesfully - Transcribing audio into text")

# Transcribe the audio
result = whisper.transcribe(model, audio, language="en")

timestamps = [(segment['start'], segment['end']) for segment in result['segments']]
transcriptions = [segment['text'] for segment in result['segments']]

with open("english_transcription.txt", "w") as file:
    for (start_time, end_time), transcription in zip(timestamps, transcriptions):
        file.write(f"{start_time}-{end_time}: {transcription}\n")

transcript = ' '.join(transcriptions)
# Define the available languages and their details
languages = [
    {"name": "English (Indian)", "code": "en-IN", "voice_male": "en-IN-Standard-B", "voice_female": "en-IN-Standard-A"},
    {"name": "Hindi", "code": "hi-IN", "voice_male": "hi-IN-Standard-B", "voice_female": "hi-IN-Standard-A"},
    {"name": "Bengali", "code": "bn-IN", "voice_male": "bn-IN-Standard-B", "voice_female": "bn-IN-Standard-A"},
    {"name": "Tamil", "code": "ta-IN", "voice_male": "ta-IN-Standard-B", "voice_female": "ta-IN-Standard-A"},
    {"name": "Telugu", "code": "te", "voice_male": "te-IN-Standard-B", "voice_female": "te-IN-Standard-A"},
    {"name": "Kannada", "code": "kn-IN", "voice_male": "kn-IN-Standard-B", "voice_female": "kn-IN-Standard-A"},
    {"name": "Malayalam", "code": "ml-IN", "voice_male": "ml-IN-Standard-B", "voice_female": "ml-IN-Standard-A"},
    {"name": "Marathi", "code": "mr-IN", "voice_male": "mr-IN-Standard-B", "voice_female": "mr-IN-Standard-A"},
    {"name": "Gujarati", "code": "gu-IN", "voice_male": "gu-IN-Standard-B", "voice_female": "gu-IN-Standard-A"},
    {"name": "Punjabi", "code": "pa-IN", "voice_male": "pa-IN-Standard-B", "voice_female": "pa-IN-Standard-A"},
    {"name": "Urdu", "code": "ur-IN", "voice_male": "ur-IN-Standard-B", "voice_female": "ur-IN-Standard-A"}
]

# Display the available languages with numbers
print("Select a language:")
for i, lang in enumerate(languages, start=1):
    print(f"{i}. {lang['name']}")

# Get user input for language selection
selected_lang = int(input("Enter the number corresponding to your desired language: ")) - 1
selected_language = languages[selected_lang]

# Prompt for male or female voice
gender = input("Choose voice gender (M/F): ").lower()
selected_voice = selected_language["voice_male"] if gender == "m" else selected_language["voice_female"]
print(selected_language["code"])

# Read the original transcript from the file
with open("english_transcription.txt", "r") as file:
    original_transcript = file.read()

translation = translate_client.translate(transcript, target_language=selected_language["code"])
# Write the translated text to a file
with open('transcript.txt', 'w', encoding='utf-8') as f:
    f.write(translation['translatedText'])


translation = translate_client.translate(original_transcript, target_language=selected_language["code"])
# Write the translated text to a file
with open('translated_transcript.txt', 'w', encoding='utf-8') as f:
    f.write(translation['translatedText'])


# Read the translated text from the file
with open('transcript.txt', 'r', encoding='utf-8') as f:
    translated_text = f.read()

# Generate Telugu audio from the translated text
synthesis_input = texttospeech.SynthesisInput(text=translated_text)
# Create the VoiceSelectionParams object
voice = texttospeech.VoiceSelectionParams(
    language_code=selected_language["code"]+"-IN",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    name=selected_voice
)

audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1.2, pitch=-2.0)
response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

print("Translated text is getting a voice now")

# Save the Telugu audio to a file
with open('translated_audio.wav', 'wb') as out:
    out.write(response.audio_content)

# # Replace the English audio in the video with the Telugu audio
input_video = ffmpeg.input('input_video1.mp4')
input_audio = ffmpeg.input('translated_audio.wav')
ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished_video.mp4').run()
