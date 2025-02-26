import os
import yt_dlp
import re
import input_params as inp
import unicodedata
import shutil

def download_youtube_video(url, save_path="./"):
    if not os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    try:        
        # Extract video information without downloading
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown Title')
            file_path = os.path.join(save_path, f"{video_title}.mp4")
            path=rename_video_path(file_path)

        # Check if the file already exists
        if os.path.exists(path):
            print(f"File already exists: {path}. Skipping download.")
            print(path)
            return path

        # Set options for downloading
        ydl_opts = {
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            ydl.download([url])

        print(f"Download completed! Video saved to: {file_path}")
        print(file_path)
        return file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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
  extracted_text = extracted_text.replace("download folder ",f"{inp.youtube_download_folder}\\" )

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
