from google.cloud import speech, translate_v2 as translate, texttospeech
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from google.cloud import storage
from pydub import AudioSegment
from scipy.io import wavfile
import io
import time
import ffmpeg
import whisper

# Initialize the GCP client for each service
speech_client = speech.SpeechClient()
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

# Load your video file and extract the audio
video = VideoFileClip('input_video1.mp4')
video.audio.write_audiofile('temp_audio.wav')

# Load the audio file
audio = whisper.load_audio("temp_audio.wav")

# Load the model
model = whisper.load_model("small", device="cpu")

print("Whisper - Model loaded Succesfully - Transcribing audio into text")

# Transcribe the audio
result = whisper.transcribe(model, audio, language="en")

# Extract timestamps and transcriptions
timestamps = [segment['start'] for segment in result['segments']]
transcriptions = [segment['text'] for segment in result['segments']]

# Write timestamps and transcriptions to a separate file
with open("transcription.txt", "w") as file:
    for timestamp, transcription in zip(timestamps, transcriptions):
        file.write(f"{timestamp}: {transcription}\n")

transcript = ' '.join(transcriptions)
translation = translate_client.translate(transcript, target_language='te')
        
print("Transcript generated - Translation process initiated")
        
# Translate the transcript to Telugu
translation = translate_client.translate(transcript, target_language='te')

# Write the translated text to a file
with open('transcript.txt', 'w', encoding='utf-8') as f:
    f.write(translation['translatedText'])

# Read the translated text from the file
with open('transcript.txt', 'r', encoding='utf-8') as f:
    translated_text = f.read()

# Generate Telugu audio from the translated text
synthesis_input = texttospeech.SynthesisInput(text=translated_text)
# voice = texttospeech.VoiceSelectionParams(language_code='te-IN', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, name='te-IN-Wavenet-A')
voice = texttospeech.VoiceSelectionParams(language_code='te-IN', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, name='te-IN-Standard-B')
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=0.9, pitch=-2.0)
response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

print("Translated text is getting a voice now")

# Save the Telugu audio to a file
with open('translated_audio.wav', 'wb') as out:
    out.write(response.audio_content)

# # Replace the English audio in the video with the Telugu audio
input_video = ffmpeg.input('input_video1.mp4')
input_audio = ffmpeg.input('translated_audio.wav')
ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished_video.mp4').run()