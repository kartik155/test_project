# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
import os
import moviepy as mp
import openai
import json
import shutil
import re
import pandas as pd
import assemblyai as aai
import tempfile
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import input_params as inp
import sys
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time 
import audio_chunks as ac
from datetime import datetime

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

assembly_ai_key= os.getenv("ASSEMBLY_AI_KEY")
open_api_key= os.getenv("OPENAI_API_KEY")


def time_frame_to_seconds(time_frame):
    h, m, s_ms = time_frame.split(':')
    if len(s_ms.split('.'))==2:
        s, ms = s_ms.split('.')
    else:
        s=s_ms
        ms=0
    total_seconds = ((int(h) * 3600) + (int(m) * 60 )+ (int(s))  + round(int(ms)/1000,0))
    return total_seconds

# Function to convert milliseconds to time frame
#{h:02}:{m:02}:{s:02},{ms:03}
def seconds_to_time_frame(seconds):
    h = int(seconds // 3600)
    seconds %= 3600
    m = int(seconds // 60)
    seconds %= 60
    s = int(seconds // 1)
    ms = int((seconds % 1)*1000)
    return f'{h:02}:{m:02}:{s:02}'

def get_today_date():
    return datetime.today().strftime("%m_%d_%Y")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def fuzzy_merge(df1, df2, key1, key2, threshold=90, limit=1):
   # Store the matches and scores in this list
    match_tuples = []

    # For each item in df1's key column, find best match in df2's key column
    for i, row in df1.iterrows():
        best_matches = process.extract(row[key1], df2[key2],
                                       scorer=fuzz.token_sort_ratio
                                       #scorer=fuzz.token_set_ratio
                                       #scorer=fuzz.partial_ratio
                                       , limit=limit)
        for match in best_matches:
            if match[1] >= threshold:
                match_row = df2[df2[key2] == match[0]].copy().reset_index(drop=True)
                for _, m in match_row.iterrows():
                    # Append the match score
                    m['Match_Score'] = match[1]
                    # Reset index before concatenating
                    combined_row = pd.concat([row.reset_index(drop=True), m], axis=0)

                    match_tuples.append(combined_row)

    # Convert list of matched rows to DataFrame
    matched_df = pd.DataFrame(match_tuples).reset_index(drop=True)

    return matched_df

def fuzzy_match(x, choices, cutoff=60):
    """
    Fuzzy matches a string against a list of choices.

    Args:
        x: The string to match.
        choices: A list of strings to compare against.
        cutoff: The minimum similarity score to consider a match.

    Returns:
        The best match or None if no match is found.
    """
    match = process.extractOne(x, choices)
    if match[1] >= cutoff:
        return match[0]
    else:
        return None

def list_files_in_folder(folder_path):
    try:
        # Get a list of files in the specified folder
        file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return file_list
    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def dataframe_to_srt(df):
    srt_content = []
    for index, row in df.iterrows():
        #start = row['Start_in_label']
        #end = row['End_in_label']
        # speaker = row['speaker_original']
        # text = row['Corrected_Text']
        speaker = row['final_speaker']
        text = row['text']

        #srt_content.append(f"{start} --> {end}\n{speaker}: {text}\n")
        srt_content.append(f"{speaker}: {text}\n")

    return '\n'.join(srt_content)


# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def transcript_chunks(video_path):
    aai.settings.api_key = assembly_ai_key

    config = aai.TranscriptionConfig(
    #  word_boost=word_boost_res,
    #  boost_param="high",
    #    language_code=language_code,
    speaker_labels=True,
    language_detection=True
    )
    transcriber = aai.Transcriber()


    file_name = os.path.splitext(os.path.basename(video_path))[0]
    file_folder=f"{inp.output_folder}/{file_name}"
    audio_chunks_folder=f"{file_folder}/audio_chunks"
    transcribed_chunks_folder=f"{file_folder}/Transcribed_chunks"
    if not os.path.exists(transcribed_chunks_folder):
        os.makedirs(transcribed_chunks_folder)
    
    required_paths=list_files_in_folder(audio_chunks_folder)
    output_paths=[]
    for i,required_path in enumerate(required_paths):
        try:
            local_file_path=f"{audio_chunks_folder}/{required_path}"
            transcript = transcriber.transcribe(local_file_path,config)
            Audio_file_west_transcription_chunk_df=pd.DataFrame()
            text_with_speaker_labels = ""
            print(transcript.utterances)
            
            for utt in transcript.utterances:
                text_with_speaker_labels += f"Speaker {utt.speaker}:\n{utt.text}\n"

            unique_speakers = set(utterance.speaker for utterance in transcript.utterances)

            questions = []
            for speaker in unique_speakers:
                questions.append(
                    aai.LemurQuestion(
                    question=f"Who is speaker {speaker}?",
                    answer_format="<First Name> <Last Name (if applicable)>"
                    )
                )

            result = aai.Lemur().question(
                questions,
                input_text=text_with_speaker_labels,
                context="Your task is to infer the speaker's name from the speaker-labelled transcript.",
                final_model=aai.LemurModel.claude3_5_sonnet
            )
            speaker_mapping = {}
            for qa_response in result.response:
                pattern = r"Who is speaker (\w)\?"
                match = re.search(pattern, qa_response.question)
                if match and match.group(1) not in speaker_mapping.keys():
                    speaker_mapping.update({match.group(1): qa_response.answer})
            for a in range(len(transcript.utterances)):
                Audio_file_west_transcription_chunk_df.loc[a,'start']=int(transcript.utterances[a].start/1000)
                Audio_file_west_transcription_chunk_df.loc[a,'end']=int(transcript.utterances[a].end/1000)
                Audio_file_west_transcription_chunk_df.loc[a,'speaker_label']=transcript.utterances[a].speaker
                Audio_file_west_transcription_chunk_df.loc[a,'speaker']=speaker_mapping[transcript.utterances[a].speaker]
                Audio_file_west_transcription_chunk_df.loc[a,'text']= transcript.utterances[a].text
        

            output_csv_filename= transcribed_chunks_folder + "/" +required_path.split(".")[0]+".csv"
            print(output_csv_filename)
            Audio_file_west_transcription_chunk_df.to_csv(output_csv_filename)
            # Audio_file_west_transcription_chunk_df.to_csv(output_csv_filename)
        except Exception as e:
            error_message= f"Failed to Transcribe the audio \n Error: {str(e)}"
            raise RuntimeError(error_message)
        


def speaker_mapping(Full_Transcript_df):
    
    unmatched_speaker_df=pd.DataFrame()
    ##### Mapping first name with their full names if present in the transcript############################
    # Standardize case for comparison
    Full_Transcript_df['speaker_llm'] = Full_Transcript_df['speaker_llm'].str.title()

    # Extract unique speakers with full names (those with more than one word)
    full_names_list = Full_Transcript_df[Full_Transcript_df['speaker_llm'].str.split().str.len() > 1]['speaker_llm'].unique()
    # Create a mapping of first name to full name
    first_to_full_name = {}
    for full_name in full_names_list:
        first_name = full_name.split()[0]
        if first_name not in first_to_full_name:
            first_to_full_name[first_name] = full_name

    # Replace only first names with corresponding full names in the main DataFrame
    Full_Transcript_df['speaker_llm'] = Full_Transcript_df['speaker_llm'].apply(
        lambda x: first_to_full_name.get(x, x) if len(x.split()) == 1 and first_to_full_name.get(x, x) not in first_to_full_name.values() else x  # Replace only if it's a first name and no ambiguity  
    )
    
    unmatched_speaker_df['speaker_llm']=Full_Transcript_df['speaker_llm'].unique()

    # Extract unique speakers with full names (those with more than one word)
    full_names = unmatched_speaker_df[unmatched_speaker_df['speaker_llm'].str.split().str.len() > 1]['speaker_llm'].unique()

    # Get the first names from the full names
    full_name_firsts = [name.split()[0] for name in full_names]

    if len(full_names)>0 and len(full_name_firsts)>0:
        # Create a new column to store matched names
        #matching the speaker having first names only with the first names from the speaker having full names
        unmatched_speaker_df['matched_name'] = unmatched_speaker_df['speaker_llm'].apply(
            lambda x: fuzzy_match(x, full_name_firsts,70) if len(x.split()) == 1 else x  # Replace only if it's a first name
        )

        # Update `matched_name` with full name if matched
        unmatched_speaker_df['matched_name'] = unmatched_speaker_df.apply(
            lambda row: next((name for name in full_names if name.startswith(row['matched_name'])), row['speaker_llm'])
            if row['matched_name'] else row['speaker_llm'],
            axis=1
        )
    else:            
        unmatched_speaker_df['matched_name']=unmatched_speaker_df['speaker_llm']

    unmatched_speaker_df['matched_name'] = unmatched_speaker_df['matched_name'].str.upper()
    # unmatched_speaker_df.rename(columns={'speaker_llm':'speaker_llm_mapper'},inplace=True)
    Full_Transcript_df = Full_Transcript_df.merge(
        unmatched_speaker_df,
        how='left',  # Left join
        on='speaker_llm',  # Column in Full_Transcript_df
        )
    Full_Transcript_df['final_speaker'] = Full_Transcript_df.apply(
    lambda row: row['matched_name'] if pd.notna(row['matched_name']) else row['speaker_llm'],
    axis=1
    )
    Full_Transcript_df['final_speaker'] = Full_Transcript_df['final_speaker'].fillna(Full_Transcript_df['speaker_llm'])
    Full_Transcript_df['final_speaker']=Full_Transcript_df['final_speaker'].str.upper()
    return Full_Transcript_df


def corrected_text(text):

    flag = 0
    for flag in range(0,3): 
        try:
            # Create a chat model (You can choose a different LLM model)
            llm = ChatOpenAI(model="gpt-4o")

            # Define a simple prompt template that includes the document as context
            prompt_template = """
            As an expert in life sciences, with a focus on medical terminology and pharmacology, 
            review the text for inaccuracies in drug names or medical terms. Correct any discrepancies to ensure 
            alignment with standard medical terminology and scientific accuracy. If no corrections are needed, 
            return the input text exactly as it is, without modifications.
            '''
            INPUT TEXT : {text}
            
            '''
            """

            # Initialize the prompt with the document content and conversation history
            prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

            # Create a ConversationChain (this will use the whole document as context)
            # qa_chain = ConversationChain.from_llm(llm, prompt)
            qa_chain= prompt | llm | StrOutputParser()

            answer = qa_chain.invoke({"text":text})

                
            return answer
        except Exception as e:
            print("Error Occurs", str(e))
            error_message=str(e)
            flag += 1
            time.sleep(1)
            continue
    if flag == 3:
        #return f"Error: {error_message}"
        raise RuntimeError(f"{error_message}")



def full_transcript(video_path):
    Audio_file_transcription=pd.DataFrame()

    file_name = os.path.splitext(os.path.basename(video_path))[0]
    file_folder=f"{inp.output_folder}/{file_name}"

    transcribed_chunks_folder=f"{file_folder}/Transcribed_chunks"
    
    combined_transcript_folder=f"{file_folder}/Full_Transcript"
    if not os.path.exists(combined_transcript_folder):
        os.makedirs(combined_transcript_folder)
    
    required_paths=list_files_in_folder(transcribed_chunks_folder)
    
    for i in range(len(required_paths)):        
        try:
            Audio_file_west_transcription_chunk_df=pd.read_csv(transcribed_chunks_folder+"/"+required_paths[i])

            Audio_file_west_transcription_chunk_df['speaker_from_Zoom']=None
            # uncomment this after getting the api key
            Audio_file_west_transcription_chunk_df['speaker_llm']=Audio_file_west_transcription_chunk_df['speaker']
            Audio_file_west_transcription_chunk_df=Audio_file_west_transcription_chunk_df[['start','end','speaker_llm','speaker_from_Zoom','speaker','text']]

            # remove this after gettinh api key
            # Audio_file_west_transcription_chunk_df['speaker_llm']=Audio_file_west_transcription_chunk_df['speaker_label']
            # Audio_file_west_transcription_chunk_df=Audio_file_west_transcription_chunk_df[['start','end','speaker_llm','speaker_from_Zoom','text']]
            
            if i==0:
                # Calculate the adjustment value
                adjustment = Audio_file_west_transcription_chunk_df.iloc[-1]['end'] - 1310
                # Update the 'start' and 'end' columns
                Audio_file_west_transcription_chunk_df['start'] -= adjustment
                Audio_file_west_transcription_chunk_df['end'] -= adjustment
            else:
                Audio_file_west_transcription_chunk_df['start']= Audio_file_west_transcription_chunk_df['start']+(1310*i)
                Audio_file_west_transcription_chunk_df['end']= Audio_file_west_transcription_chunk_df['end']+(1310*i)
            Audio_file_west_transcription_chunk_df['Start_in_label']=Audio_file_west_transcription_chunk_df['start'].apply(seconds_to_time_frame)
            Audio_file_west_transcription_chunk_df['End_in_label']=Audio_file_west_transcription_chunk_df['end'].apply(seconds_to_time_frame)
    #         Audio_file_transcription=Audio_file_transcription.append(Audio_file_west_transcription_chunk_df)
            Audio_file_transcription=pd.concat([Audio_file_transcription,Audio_file_west_transcription_chunk_df],ignore_index=True)
            Audio_file_transcription['speaker_llm'] = Audio_file_transcription['speaker_llm'].apply(
            lambda x: x[4:] if isinstance(x, str) and x.lower().startswith('dr. ') else x
            )    
            Transcript_df=speaker_mapping(Audio_file_transcription)
            
            # Transcript_df['Corrected_Text']=Transcript_df['text'].apply(corrected_text)

            # transcript_file_path=f"{combined_transcript_folder}/transcirpt_df.csv"
            # Transcript_df.to_csv(transcript_file_path)
            
            clean_transcript = dataframe_to_srt(Transcript_df)
            
            with open(f"{combined_transcript_folder}/Transcript.txt", 'w') as file:
                file.write(clean_transcript)
            print("Transcript is successfully created")
            return clean_transcript
        except Exception as e:
            error_message=f"Failed to append the transcribed chunks to full transcript.\n Error: {e}"
            raise RuntimeError(error_message)



def transcription(video_path):
    filename = os.path.basename(video_path)+f'_{get_today_date()}'
    video_name=os.path.splitext(filename)[0]
    
    transcript_path = os.path.join(inp.output_folder, video_name, "Full_Transcript", "Transcript.txt")
    
    if os.path.exists(transcript_path):
        # st.write("Video already Transcribed")
        with open(transcript_path, 'r') as f:
            return f.read()
        
    else:            
        ac.audio_chunking(video_path)
        transcript_chunks(video_path)
        transcript=full_transcript(video_path)
        return transcript