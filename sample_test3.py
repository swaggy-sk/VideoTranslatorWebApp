from google.cloud import speech, translate_v2 as translate, texttospeech
from google.cloud import storage
from pydub import AudioSegment
from scipy.io import wavfile
import io
import time
import subprocess
import ffmpeg
import whisper
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import shutil
import os
import subprocess

# Initialize the GCP client for each service
speech_client = speech.SpeechClient()
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

def browse_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if selected_file_path:
        selected_file_label.config(text=selected_file_path)

# Function to handle submission
def submit():
    global is_translating
    is_translating = True
    input_language = input_language_var.get()
    voice_type = voice_type_var.get()
    output_language = output_language_var.get()
    
    # Move the selected file to the project folder
    if selected_file_path:
        file_name = os.path.basename(selected_file_path)
        destination_path = os.path.join(os.getcwd(), file_name)
        
        # Check if the source and destination paths are the same
        if selected_file_path != destination_path:
            shutil.copy(selected_file_path, destination_path)
            
            # Convert the video to MP3
            audio_file_path = os.path.splitext(destination_path)[0] + ".mp3"
            convertVideoToMp3(selected_file_path, audio_file_path)
            
            # Generate Transcription
            trascript_and_trans(audio_file_path)
        else:
            messagebox.showerror("Error", "Please choose a different destination path.")
    
    # Backend processing here...
    # messagebox.showinfo("Processing", "Audio file is being generated...")

# Function to update the message after translation
def update_message():
    global is_translating
    if is_translating:
        messagebox.showinfo("Translation", "Translation is done successfully! You can download the file now.")
        is_translating = False

# Function to handle file download
def download():
    # Prompt the user to select the path to save the file
    save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

    if save_path:
        # Run ffmpeg command to concatenate video and audio
        input_video = ffmpeg.input(selected_file_path)
        input_audio = ffmpeg.input('translated_audio.wav')
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(save_path).run()
        
        messagebox.showinfo("Download", "File downloaded successfully! Now you can close this window")


# Load your video file and extract the audio
def convertVideoToMp3(input_file, output_file):
    ffmpeg_cmd = ["ffmpeg", "-i", input_file, "-vn", "-acodec", "libmp3lame", "-ab", "192k", "-ar", "44100", "-y", output_file]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Successfully Converted")
    except subprocess.CalledProcessError as e:
        print("Conversion error")


def trascript_and_trans(audio_file_path):
    # Load the audio file
    # audio = whisper.load_audio("temp_audio.wav")
    audio = whisper.load_audio(audio_file_path)

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
        {"name": "English (Indian)", "code": "en", "voice_male": "en-IN-Standard-B", "voice_female": "en-IN-Standard-A"},
        {"name": "Hindi", "code": "hi", "voice_male": "hi-IN-Standard-B", "voice_female": "hi-IN-Standard-A"},
        {"name": "Bengali", "code": "bn", "voice_male": "bn-IN-Standard-B", "voice_female": "bn-IN-Standard-A"},
        {"name": "Tamil", "code": "ta", "voice_male": "ta-IN-Standard-B", "voice_female": "ta-IN-Standard-A"},
        {"name": "Telugu", "code": "te", "voice_male": "te-IN-Standard-B", "voice_female": "te-IN-Standard-A"},
        {"name": "Kannada", "code": "kn", "voice_male": "kn-IN-Standard-B", "voice_female": "kn-IN-Standard-A"},
        {"name": "Malayalam", "code": "ml", "voice_male": "ml-IN-Standard-B", "voice_female": "ml-IN-Standard-A"},
        {"name": "Marathi", "code": "mr", "voice_male": "mr-IN-Standard-B", "voice_female": "mr-IN-Standard-A"},
        {"name": "Gujarati", "code": "gu", "voice_male": "gu-IN-Standard-B", "voice_female": "gu-IN-Standard-A"},
        {"name": "Punjabi", "code": "pa", "voice_male": "pa-IN-Standard-B", "voice_female": "pa-IN-Standard-A"},
        {"name": "Urdu", "code": "ur", "voice_male": "ur-IN-Standard-B", "voice_female": "ur-IN-Standard-A"}
    ]

        # Print the selected input language
    print("Selected Input Language:", input_language_var.get())

    # Print the selected output language
    print("Selected Output Language:", output_language_var.get())

    # Print the selected voice type
    print("Selected Voice Type:", voice_type_var.get())

    # Print the selected file path
    print("Selected File Path:", selected_file_path)

    # Print the translation status
    print("Translation Status:", is_translating)

    # Display the available languages with numbers
    # print("Select a language:")
    # for i, lang in enumerate(languages, start=1):
    #     print(f"{i}. {lang['name']}")

    # Get user input for language selection
    # selected_lang = int(input("Enter the number corresponding to your desired language: ")) - 1
    # selected_lang = output_language_var.get()
    
    # selected_language = languages[selected_lang]

    selected_lang = output_language_var.get()

    selected_language = None
    for lang in languages:
        if lang["name"] == selected_lang:
            selected_language = lang
            break

    language_code = selected_language["code"]
    
    # Prompt for male or female voice
    # gender = input("Choose voice gender (M/F): ").lower()
    gender = voice_type_var.get()
    
    selected_voice = selected_language["voice_male"] if gender == "Male" else selected_language["voice_female"]
    # print(selected_language["code"])

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
    print("Translated text is getting a voice now")

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

    # Save the Telugu audio to a file
    with open('translated_audio.wav', 'wb') as out:
        out.write(response.audio_content)
        
    messagebox.showinfo("Translation", "Translation succesfull, You can Download the File Now !")
    



# Main Tkinter window
root = tk.Tk()
root.title("Video Translator")

# Frames
frame_file = ttk.Frame(root)
frame_language = ttk.Frame(root)
frame_buttons = ttk.Frame(root)

frame_file.pack(pady=20)
frame_language.pack(pady=20)
frame_buttons.pack(pady=20)

# File Selection
selected_file_label = ttk.Label(frame_file, text="No file selected", font=("Helvetica", 14))
selected_file_label.pack(side="left", padx=20)
browse_button_style = ttk.Style()
browse_button_style.configure("Browse.TButton", font=("Helvetica", 14))
browse_button = ttk.Button(frame_file, text="Browse", command=browse_file, style="Browse.TButton")
browse_button.pack(side="left", padx=20)

# Language Selection
input_language_var = tk.StringVar()
output_language_var = tk.StringVar()
voice_type_var = tk.StringVar()

# input_language_label = ttk.Label(frame_language, text="Input Language:", font=("Helvetica", 14))
# input_language_label.grid(row=0, column=0, padx=20, pady=20)
# input_language_dropdown = ttk.Combobox(frame_language, textvariable=input_language_var, state="readonly", font=("Helvetica", 14))
# input_language_dropdown['values'] = (
#     "English","Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Catalan", "Chinese",
#     "Croatian", "Czech", "Danish", "Dutch",  "Estonian", "Finnish", "French", "Galician", "German",
#     "Greek", "Hebrew", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh",
#     "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Maori", "Nepali", "Norwegian", "Persian",
#     "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish",
#     "Tagalog", "Thai", "Turkish", "Ukrainian", "Vietnamese", "Welsh"
# )
# input_language_dropdown.grid(row=0, column=1, padx=20, pady=20)

voice_type_label = ttk.Label(frame_language, text="Voice Type:", font=("Helvetica", 14))
voice_type_label.grid(row=1, column=0, padx=20, pady=20)
voice_type_dropdown = ttk.Combobox(frame_language, textvariable=voice_type_var, state="readonly", font=("Helvetica", 14))
voice_type_dropdown['values'] = ("Male", "Female")
voice_type_dropdown.grid(row=1, column=1, padx=20, pady=20)

output_language_label = ttk.Label(frame_language, text="Output Language:", font=("Helvetica", 14))
output_language_label.grid(row=2, column=0, padx=20, pady=20)
output_language_dropdown = ttk.Combobox(frame_language, textvariable=output_language_var, state="readonly", font=("Helvetica", 14))
output_language_dropdown['values'] = (
    "Hindi", "Bengali", "Gujarati", "Kannada", "Malayalam", "Marathi", "Tamil", "Telugu", "Urdu"
)
output_language_dropdown.grid(row=2, column=1, padx=20, pady=20)

# Buttons
submit_button = ttk.Button(frame_buttons, text="Submit", command=submit, style="Browse.TButton")
submit_button.pack(side="left", padx=20)
download_button = ttk.Button(frame_buttons, text="Download", command=download, style="Browse.TButton")
download_button.pack(side="left", padx=20)

# Call update_message() after a delay of 10 seconds (10000 milliseconds)
root.after(10000, update_message)

root.mainloop()
