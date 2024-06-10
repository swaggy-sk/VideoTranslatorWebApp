# Video Translator

This application allows you to upload an MP4 video, extract the audio, transcribe it, translate the transcription into various languages, and generate an audio file in the selected language. The translated audio can then be merged back with the original video.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Required Libraries](#required-libraries)
3. [GCP Account and API Keys](#gcp-account-and-api-keys)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)

## System Requirements

- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux
- Google Cloud Platform (GCP) account

## Required Libraries

Make sure you have the following libraries installed before running the application:

- google-cloud-speech
- google-cloud-translate
- google-cloud-texttospeech
- google-cloud-storage
- pydub
- scipy
- ffmpeg-python
- whisper
- tkinter
- shutil
- os
- subprocess

You can install these libraries using pip:

```bash
pip install google-cloud-speech google-cloud-translate google-cloud-texttospeech google-cloud-storage pydub scipy ffmpeg-python whisper
````

## GCP Account and API Keys

1. **Create a GCP Account:** If you don't have a GCP account, create one [here](https://cloud.google.com/).

2. **Enable APIs:**
    - Go to the GCP Console and enable the following APIs:
        - Cloud Speech-to-Text API
        - Cloud Translation API
        - Cloud Text-to-Speech API
        - Cloud Storage API

3. **Create Service Account and Download Key:**
    - Create a service account in the GCP Console.
    - Grant the necessary permissions to the service account.
    - Download the service account key (JSON file).

4. **Set Environment Variable:**
    - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file. For example:
    
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
    ```

## Installation

1. **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install Required Libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Download ffmpeg:**
    - Download and install ffmpeg from [here](https://ffmpeg.org/download.html).
    - Add ffmpeg to your system PATH.

## Usage

1. **Run the Application:**

    ```bash
    python video_translator.py
    ```

2. **Select the MP4 File:**
    - Click on the "Browse" button to select the MP4 video file you want to translate.

3. **Select Output Language and Voice Type:**
    - Choose the desired output language from the dropdown menu.
    - Choose the desired voice type (Male or Female).

4. **Submit the File:**
    - Click on the "Submit" button to start the translation process.
    - The application will extract the audio, transcribe it, translate the transcription, and generate the translated audio.

5. **Download the Translated Video:**
    - Click on the "Download" button to save the video with the translated audio.

## Troubleshooting

- **ffmpeg not found:**
  - Make sure ffmpeg is installed and added to your system PATH.

- **Google Cloud API Errors:**
  - Ensure your service account key file is correctly set in the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
  - Check if the required APIs are enabled in your GCP project.

- **Library Installation Issues:**
  - Ensure all required libraries are installed. You can install missing libraries using pip.

## Contributing

If you have any suggestions or improvements, feel free to create a pull request or open an issue.

## Publication

This project is published on https://www.ijisrt.com/harnessing-open-innovation-for-translating-global-languages-into-indian-lanuages



This README provides clear instructions for setting up and running your application, ensuring that even beginners can follow along without any issues.
