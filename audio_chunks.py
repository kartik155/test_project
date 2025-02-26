import os.path
import pandas as pd, numpy as np
import os
import moviepy as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
# from moviepy.editor import AudioFileClip
import openai
import json
import shutil
import re
import pandas as pd
import assemblyai as aai
import audiofile as af
import tempfile
# from docx import Document
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import time
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3, EasyMP3
import input_params as inp


# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Converting audio files to binary data
def mp3_to_audio_bytes(mp3_file_path):
    #audio = AudioSegment.from_mp3(mp3_file_path)
    #audio_bytes = audio.raw_data
    with open(mp3_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    return audio_data

def mp4_to_mp3(input_mp4):
    try:
        # Create a temporary file for audio extraction
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            video = AudioFileClip(input_mp4)
            video.write_audiofile(temp_file.name)

        # Read the audio data from the temporary file
        with open(temp_file.name, "rb") as f:
            audio_data = f.read()

    except FileNotFoundError:
        raise FileNotFoundError(f"Input MP4 file not found: {input_mp4}")
    finally:
        # Clean up the temporary file (if created)
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)

    return audio_data

def m4a_to_mp3(input_m4a):
    try:
        # Create a temporary file for MP3 conversion
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            audio = AudioFileClip(input_m4a)
            audio.write_audiofile(temp_file.name)

        # Read the MP3 audio data from the temporary file
        with open(temp_file.name, "rb") as f:
            mp3_bytes = f.read()

    except FileNotFoundError:
        raise FileNotFoundError(f"Input M4A file not found: {input_m4a}")
    finally:
        # Clean up the temporary file (if created)
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)

    return mp3_bytes

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#splitting the audio (binary data into chunks)
def read_and_split_audio(audio_data, chunk_size):
    # Calculate the number of chunks needed
    total_size = len(audio_data)
    num_chunks = total_size // chunk_size + (1 if total_size % chunk_size != 0 else 0)

    chunks = [audio_data[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]

    return chunks

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#converting binday data to mp3
def save_binary_data_to_mp3(binary_data, output_file):
    with open(output_file, 'wb') as mp3_file:
        mp3_file.write(binary_data)
    print(f"MP3 file saved to {output_file}")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#creating chunks
#Converting the audio file to binary data and the creating chunks of the audio file
def audio_to_binary(path):
    chunk_size = 20 * 1024 * 1024
    flag=0
    for flag in range(0,3):
        try:
            
            if path[-3:]=='mp4':
                    audio_data=mp4_to_mp3(path)
                    audio_chunks= read_and_split_audio(audio_data, chunk_size)
                    print("mp4 file successfully converted to binary data")
            elif path[-3:]=='mp3':

                    audio_data=mp3_to_audio_bytes(path)
                    audio_chunks= read_and_split_audio(audio_data, chunk_size)
                    print("mp3 file successfully converted to binary data")


            elif path[-3:]=='m4a':

                    audio_data=m4a_to_mp3(path)
                    audio_chunks= read_and_split_audio(audio_data, chunk_size)
                    print("mp4a file successfully converted to binary data")
            return audio_chunks
            # else:
            #     print("Unknown file format")

        except Exception as e:
                print("Error Occurs", str(e))
                error_message=str(e)
                flag += 1
                time.sleep(1)
                continue
    if flag == 3:
        error_message= f"Failed to convert the audio file into binary data \n Error: {error_message}"
        raise RuntimeError(error_message)



# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#Converting the binary chunks to mp3 and uploading it in the folder "Audio_chunks"


def binary_to_audio_chunks(audio_chunks,video_path):
    file_name = os.path.splitext(os.path.basename(video_path))[0]
    folder=f"{inp.output_folder}/{file_name}/audio_chunks/"
    # audio_chunks_df=pd.DataFrame()
    try:
        for i, chunk in enumerate(audio_chunks):
            output_file = "/output_audio_"+str(i+1)+".mp3"
            # audio_chunks_df.loc[i,'Filename']=output_file
            # with tempfile.TemporaryDirectory() as tmpdirname:
            local_file_path = folder + output_file
            #Create file localy
            if not os.path.exists(os.path.dirname(local_file_path)):
                os.makedirs(os.path.dirname(local_file_path))
            try:
                save_binary_data_to_mp3(chunk,local_file_path)
                # audio = MP3(local_file_path)
                # audio_chunks_df.loc[i,'Duration']=audio.info.length
                print("successfully converted binary data in audio_chunks")
            except Exception as e:
                print(f"Failed to convert binary chunks into mp3 \n Error Occurs : {str(e)}")
            # with open(local_file_path,'rb') as f:
            #     Audio_chunks_folder.upload_stream(output_file, f)
    except Exception as e:
            error_message=f"Failed to upload the audio chunks in folder \n Error Occurs : {str(e)}"
            raise RuntimeError(error_message)

def audio_chunking(video_path):
    audio_chunks=audio_to_binary(video_path)
    binary_to_audio_chunks(audio_chunks,video_path)