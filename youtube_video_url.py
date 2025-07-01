import os
import re
import unicodedata
import streamlit as st
import shutil
import time
import subprocess
import sys
import subprocess
 
def upgrade_package(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", pkg])
 
def download_youtube_video(url, save_path="./"):
    upgrade_package("yt_dlp")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    import yt_dlp
   
    format_strategies = [
        # Strategy 1: Most compatible
        'best',
        # Strategy 2: Original strategy
        'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',    
        # Strategy 3: Alternative format selection
        'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
       
    ]
    for attempt, format_strategy in enumerate(format_strategies):
        try:
            # Extract video information without downloading
            ydl_opts_start={'quiet': True,
                    'cookiefile': 'cookies.txt',  # Path to your cookies file
                      }
            print(ydl_opts_start)
            with yt_dlp.YoutubeDL(ydl_opts_start) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                video_title = info.get('title', 'Unknown Title')
                file_path = os.path.join(save_path, f"{video_title}.mp4")
                path = rename_video_path(file_path)  # Ensure rename function exists
 
            # Check if the file already exists
            if os.path.exists(path):
                print(f"File already exists: {path}. Skipping download.")
                return path
 
            # Set options for downloading
            ydl_opts = {
                'format': format_strategy,
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                # 'cookiefile': 'cookies.txt',  # Path to your cookies file
                'verbose': True,  # Enable verbose output for debugging
                }
 
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading video from: {url}")
                ydl.download([url])
 
            print(f"Download completed! Video saved to: {file_path}")
            return file_path  # Exit loop if successful
 
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < len(format_strategies) - 1:
                time.sleep(5)
 
    # If both attempts fail, raise an error
    raise RuntimeError("Download failed after all the attempts. Check the YouTube URL or internet connection.")
 
 
def extract_text_and_numbers(filename):
  """
  Extracts text and numbers from a filename with spaces between them.
 
  Args:
    filename: The original filename.
 
  Returns:
    A string containing only text and numbers from the filename with spaces between them.
  """
  # Normalize Unicode characters (convert full-width characters to ASCII)
  filename = unicodedata.normalize("NFKC", filename)
  # Regular expression to match text and numbers
  pattern = r"[a-zA-Z0-9]+"
 
  # Find all matches of the pattern in the filename
  matches = re.findall(pattern,filename)
 
  # Join the matches with spaces
  extracted_text = " ".join(matches)
 
  # Replace "mp4" with ".mp4"
  extracted_text = extracted_text.replace(" mp4", ".mp4")        
  extracted_text = extracted_text.replace("download folder ","downloaded_video\\" )
 
  return extracted_text
 
 
def rename_files(directory):
  """
  Renames files in the given directory by replacing fullwidth vertical bar (｜) with standard vertical bar (|).
 
  Args:
    directory: Path to the directory containing the files.
  """
  for filename in os.listdir(directory):
    old_path = os.path.join(directory, filename)
    new_filename=extract_text_and_numbers(filename)      
    new_path = os.path.join(directory, new_filename)
    os.rename(old_path, new_path)
    print(f"Renamed '{old_path}' to '{new_path}'")
  return new_path
 
def rename_video_path(video_path):
    """
    Applies `extract_text_and_numbers` only on the filename, keeping the directory structure intact.
 
    Args:
        video_path (str): Full path of the video file.
 
    Returns:
        str: The cleaned full path.
    """
    # Separate directory and filename
    directory, filename = os.path.split(video_path)
 
    # Process only the filename
    new_filename = extract_text_and_numbers(filename)
 
    # Construct the new full path
    new_video_path = os.path.join(directory, new_filename)
 
    return new_video_path
 
