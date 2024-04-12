import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import shutil
import os
import subprocess

# Function to handle file selection
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
        else:
            messagebox.showerror("Error", "Please choose a different destination path.")
    
    # Backend processing here...
    messagebox.showinfo("Translation", "Video file is being generated...")

# Function to update the message after translation
def update_message():
    global is_translating
    if is_translating:
        messagebox.showinfo("Translation", "Translation is done successfully! You can download the file now.")
        is_translating = False

# Function to handle file download
def download():
    # Backend processing for file download
    messagebox.showinfo("Download", "File downloaded successfully!")

# Load your video file and extract the audio
def convertVideoToMp3(input_file, output_file):
    ffmpeg_cmd = ["ffmpeg", "-i", input_file, "-vn", "-acodec", "libmp3lame", "-ab", "192k", "-ar", "44100", "-y", output_file]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Successfully Converted")
    except subprocess.CalledProcessError as e:
        print("Conversion error")

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

input_language_label = ttk.Label(frame_language, text="Input Language:", font=("Helvetica", 14))
input_language_label.grid(row=0, column=0, padx=20, pady=20)
input_language_dropdown = ttk.Combobox(frame_language, textvariable=input_language_var, state="readonly", font=("Helvetica", 14))
input_language_dropdown['values'] = (
    "English","Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Catalan", "Chinese",
    "Croatian", "Czech", "Danish", "Dutch",  "Estonian", "Finnish", "French", "Galician", "German",
    "Greek", "Hebrew", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada", "Kazakh",
    "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Maori", "Nepali", "Norwegian", "Persian",
    "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish",
    "Tagalog", "Thai", "Turkish", "Ukrainian", "Vietnamese", "Welsh"
)
input_language_dropdown.grid(row=0, column=1, padx=20, pady=20)

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
