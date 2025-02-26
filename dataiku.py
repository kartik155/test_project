import dataikuapi
import os.path
import pandas as pd
import io #to keep the data in the strcutured format 
import os
import streamlit as st
import tempfile
from io import BytesIO
import input_params as inp
from datetime import datetime

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

open_api_key= os.getenv("OPENAI_API_KEY")
dataiku_url=os.getenv("DATAIKU_URL")
dataiku_api_key = os.getenv("DATAIKU_API_KEY")

client = dataikuapi.DSSClient(dataiku_url, dataiku_api_key,no_check_certificate=True)
project = client.get_project("HAWKAI")


def get_today_date():
    return datetime.today().strftime("%m_%d_%Y")

def get_filename():
    folder=project.get_managed_folder("TAICxz8D")
    file_list = folder.list_contents()['items']
    print(file_list)
    mp_file_name = next(
        (os.path.splitext(os.path.basename(item['path']))[0] for item in file_list 
        if item['path'].lower().endswith(('.mp3', '.mp4', '.m4a'))), 
        ""
    )
    return mp_file_name+ f'_{str(get_today_date())}'

def convert_df_to_excel(df):
    # Use BytesIO to handle the file in-memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()


def delete_files(folder):
    x=folder.list_contents()
    for items in x['items']:
        folder.delete_file(items['path'])

def upload_files(path):
    folder = project.get_managed_folder("TAICxz8D")
    # delete_files(folder)  # Assuming this function clears previous files
    if os.path.isfile(path):  # If `path` is a single file
        filename = os.path.basename(path)  # Get file name
        if not filename.lower().endswith(".txt"):  # Skip deletion for .txt files
            delete_files(folder)  # Clear previous files
            with open(path, "rb") as file:
                filename = os.path.basename(path)  # Get file name
                folder.put_file(filename, file)
        print(f"Uploaded file: {filename}")
        with open(path, "rb") as file:
            folder.put_file(filename, file)
        print(f"Uploaded file: {filename}")
        if filename.lower().endswith(".txt"):  
            recipe = project.get_recipe('compute_input_files')
            recipe.run()
            print("Compute input files recipe executed succesfully") 

    if os.path.isfile(path):  # If `path` is a single file
        with open(path, "rb") as file:
            filename = os.path.basename(path)  # Get file name
            folder.put_file(filename, file)
        print(f"Uploaded file: {filename}")

    elif os.path.isdir(path):  # If `path` is a folder
        delete_files(folder)
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):  # Ensure it's a file, not a subfolder
                with open(file_path, "rb") as file:
                    folder.put_file(filename, file)
        print("All files in the folder uploaded successfully")
        


def clean_transcript():        
    # mp_file_name = next((f for f in os.listdir(input_folder) if f.endswith((".mp3","mp4","m4a"))), None)
    folder=project.get_managed_folder("TAICxz8D")
    file_list = folder.list_contents()['items']
    print(file_list)
    mp_file_name = next(
        (os.path.splitext(os.path.basename(item['path']))[0] for item in file_list 
        if item['path'].lower().endswith(('.mp3', '.mp4', '.m4a'))), 
        ""
    )
    transcript_path=inp.output_folder+f'\{mp_file_name}_'+str(get_today_date())
    os.makedirs(transcript_path,exist_ok=True)
    txt_file_name = mp_file_name + ".txt"
    txt_file_path = os.path.join(transcript_path,txt_file_name)
    csv_file_name = mp_file_name + ".csv"
    csv_file_path = os.path.join(transcript_path, csv_file_name)


    # if os.path.exists(txt_file_name) and os.path.exists(csv_file_name):
    #     print('skipping the scenario process. Files already exists')   
    #     with open(txt_file_name, "rb") as file:
    #          text= file.read()  
    # else:
    
    scenario=project.get_scenario("TRANSCRIPT_SCENARIO")
    scenario.run_and_wait()    
    transcript_folder=project.get_managed_folder("trbcMY5X")
    file=transcript_folder.get_file("Clean_Transcript.txt")
    text=file.content.decode("utf-8")
    csv_file=transcript_folder.get_file("Clean_Transcript_df.csv")
    
    df = pd.read_csv(io.StringIO(csv_file.content.decode("utf-8")))
    with open(txt_file_path, "w", encoding="utf-8") as file:
        file.write(text)
    df.to_csv(csv_file_path,index=False)
    # st.download_button("Download Cleaned Transcript",text, file_name="Clean_Transcript.txt", mime="text/plain")
    
    print(f"Clean Transcript is created and saved to {txt_file_path}")
    # st.success(f"Clean Transcript is created and saved to {txt_file_path}")

    return text

def quote_bank():
    input_folder=project.get_managed_folder("TAICxz8D")
    file_list = input_folder.list_contents()['items']
    print(file_list)
    mp_file_name = next(
        (os.path.splitext(os.path.basename(item['path']))[0] for item in file_list 
        if item['path'].lower().endswith(('.mp3', '.mp4', '.m4a'))), 
        ""
    )
    folder_path=inp.output_folder+f'\{mp_file_name}_'+str(get_today_date())
    csv_file_name = mp_file_name + '_Final_Data' + ".csv"
    csv_file_path = os.path.join(folder_path, csv_file_name)    
    scenario=project.get_scenario("FINAL_DATASET_SCENARIO")
    scenario.run_and_wait()  
    final_data_folder=project.get_managed_folder("Ir4GhfIY")
    final_dataset=final_data_folder.get_file("Final_Transcript_Data_df.csv")
    df = pd.read_csv(io.StringIO(final_dataset.content.decode("utf-8")))
    df.to_csv(csv_file_path,index=False)
    excel_data=convert_df_to_excel(df)
    st.download_button(
        label="Download the Final data",
        data=excel_data,
        file_name=csv_file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    return df
