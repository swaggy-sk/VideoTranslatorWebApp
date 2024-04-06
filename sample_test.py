from google.cloud import speech, translate_v2 as translate, texttospeech
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from scipy.io import wavfile
from spleeter.separator import Separator
import io
import time
import ffmpeg

def main():
    # Separate the vocals and music
    separator = Separator('spleeter:2stems')
    separator.separate_to_file('temp_audio.wav', 'output_directory')
    
    # The separated music will be in 'output_directory/temp_audio_mono/accompaniment.wav'
    background_music = AudioSegment.from_wav('output_directory/temp_audio_mono/accompaniment.wav')

    # Load the translated audio
    translated_audio = AudioSegment.from_wav('translated_audio.wav')

    # Mix the translated audio with the background music
    mixed_audio = translated_audio.overlay(background_music)

    # Save the mixed audio to a file
    mixed_audio.export('mixed_audio.wav', format='wav')

    # Replace the English audio in the video with the mixed audio
    mixed_audio_clip = AudioFileClip('mixed_audio.wav')
    final_video = video.set_audio(mixed_audio_clip)
    final_video.write_videofile('translated_video.mp4')
    
if __name__ == '__main__':
    main()


