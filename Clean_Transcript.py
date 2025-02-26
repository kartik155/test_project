import streamlit as st
import QnA_model as qna
import os
import tempfile
import base64
import time
import yaml
from yaml.loader import SafeLoader
import input_params as inp
import dataiku as di
import os
import youtube_video_url as yvu
import transcript as trans
from datetime import datetime
def Clean_Transcript():
    custom_css=f"""
    <style>
    [data-testid="stMainBlockContainer"] {{
        width: 100%;
        padding: 0rem 1rem 5rem;

    }}

    [data-testid="stBottomBlockContainer"] 
    {{
        width: 100%;
        padding: 0rem 1rem 4rem;
    }}
    </style>
    """

    st.markdown(custom_css,unsafe_allow_html=True)
    
    avatars = {
    "assistant" : "gemini-logo.svg",
    "user": "VG.png"
    }
    

    main_cols = st.columns(8)
    with main_cols[0]:
        st.write("")
        st.image('Header_logo.png', width=150)

    with main_cols[7]:
        st.write("")
        st.write("")
        st.write("")
        st.image("BGNE_BIG.svg", width=150)





    # Custom CSS for styling
    st.markdown(""" 
        <style>
            /* Welcome Message */
            .welcome-message {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 200px; /* Adjust height to the container's height */
                font-size: 50px;
                font-weight: bold;
                color: #2B7795; 
            text-align: center;
                margin-top: 50px; /* Optional: Adds spacing above */
            }
            .header{
                vertical-align: text-top;
                }
            /* Url Input */
            .stTextInput {
                background: #f3f2f0;
                /*border-radius: 10px;*/
            /* padding: 8px; */
                /*border: 2px solid #2B7795;*/
            }
            /* Primary Buttons */
            button[kind="primary"] {
                background-color: transparent;
                border: 2px solid #2B7795; 
                color: #2B7795; 
                font-size:
                padding: 16px 40px;
                border-radius: 8px;
                cursor: pointer;
                height: 48px; 
            }

            button[kind="primary"]:hover {
                background-color: #15396F;
                color: white;
                border-color: #15396F;
            }    
            
            /* Buttons */
            button[kind="secondary"] {
                background-color: #2B7795;
                border: none;
                color: white;
                font-size: 16px;
                padding: 8px 20px;
                border-radius: 8px;
                cursor: pointer;
                height: 48px;
            }
            button[kind="secondary"]:hover {
                background-color: #15396F;
                color: white;
            }
                        .starter-questions-header {
            font-size: 24px;
            font-weight: bold;
            color: #2B7795; /* Set the color */
            text-align: center; /* Center the text */
            text-transform: uppercase; /* Transform text to uppercase */    
            position: relative; /* Positioning for pseudo-elements */
        }
        
        .starter-questions-header::before, .starter-questions-header::after {
            content: "";
            position: absolute;
            top: 50%;
            transform: translateY(-50%); /* Ensure proper vertical alignment */    
            width: calc(50% - 80px); /* Dynamic length relative to the text */
            border-bottom: 2px solid #2B7795; /* Line color */
            display: inline-block;
        }

        .starter-questions-header::before {
            left: 0;
        }

        .starter-questions-header::after {
            right: 0;
        }    
    </style>
    """, unsafe_allow_html=True)


    if 'transcript' not in st.session_state:
        st.session_state.transcript = None

    # Initialize Session State for Chat History
    if 'hist_list' not in st.session_state:
        st.session_state.hist_list = []
    if 'hist' not in st.session_state:
        st.session_state.hist = ""

    if 'welcome_message' not in st.session_state:
        st.session_state.welcome_message = True

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = True
    if 'process' not in st.session_state:
        st.session_state.process=False
    if 'uploaded' not in st.session_state:
        st.session_state.uploaded=None
    if 'starter_question' not in st.session_state:
        st.session_state.starter_question=None
    if 'starter_question_display' not in st.session_state:
        st.session_state.starter_question_display="No"
    if 'clean_transcript' not in st.session_state:
        st.session_state.clean_transcript=None
    if 'upload' not in st.session_state:
        st.session_state.upload=None
    if 'upload_button' not in st.session_state:
        st.session_state.upload_button=False
    if "upload_option" not in st.session_state:
        st.session_state.upload_option = False
    if "video_path" not in st.session_state:
        st.session_state.video_path = False
        
    # def clear_chat_history():
    #     st.session_state.hist_list = []
    #     st.session_state.hist = ""

    def upload_button():
        st.session_state.upload_button=True
    def process():
        st.session_state.process = True
        st.session_state.hist_list = []
        st.session_state.hist = ""

    # def download_clean_trascript():
    #     st.session_state.uploaded=None
    def q1():
        st.session_state.starter_question="Give me a one page summary on the shared content"
        st.session_state.starter_question_display="No"

    def q2():
        st.session_state.starter_question="Provide detailed notes for the content shared above"
        st.session_state.starter_question_display="No"

    def is_valid_file(file_name):
        allowed_extensions = {"mp3", "mp4", "m4a"}
        return file_name.split(".")[-1].lower() in allowed_extensions
    
    inp_cols=st.columns([0.8,0.2],vertical_alignment='top')
    with inp_cols[0]:    
        # Define dynamic label before the toggle
        toggle_label = "📂 Switch to Uploading Files" if st.session_state.upload_option else "🔗 Switch to YouTube URL Input"
        # Toggle button with the correct label
        upload_option = st.toggle(toggle_label, value=st.session_state.upload_option)

    with inp_cols[1]:
        # List of top 5 European languages
        languages = ["English", "Italian","Russian", "German", "French"]
        # Dropdown with default value as "English"
        selected_language = st.selectbox("Select transcription language:", languages, index=languages.index("English"))


    # Update session state immediately
    if upload_option != st.session_state.upload_option:
        st.session_state.upload_option = upload_option
        st.rerun()  # Force Streamlit to refresh and update the label instantly


    if not st.session_state.upload_option:  # Default: Upload Files
        # st.write("Uploading files")
        uploaded_files = st.file_uploader("Upload your files", accept_multiple_files=True)
        if uploaded_files and st.session_state.upload_button==True:
            temp_dir = inp.downloaded_folder
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            for uploaded_file in uploaded_files:
                if is_valid_file(uploaded_file.name):
                    
                    file_path = os.path.join(temp_dir,uploaded_file.name)
                    st.session_state.video_path=file_path
                    # Save file to temp folder
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Call the function to upload files
                # di.upload_files(temp_dir)
                st.session_state.uploaded="All Files uploaded successfully!"
                # st.write(file_path)
            
                # st.success(st.session_state.uploaded)
    else:  # Upload YouTube Link
        # st.write("Paste YouTube URL")
        youtube_link = st.text_input("Paste YouTube link")
        # st.write(youtube_link)
        if youtube_link and st.session_state.upload_button==True:
            temp_dir=inp.downloaded_folder
            # with tempfile.TemporaryDirectory() as temp_dir:
                # Download video to the temporary directory
            # st.write(temp_dir)
            video_path = yvu.download_youtube_video(youtube_link, temp_dir)
            # st.write(video_path)
            # Rename the video file
            video_path = yvu.rename_video_path(video_path)
            print(f"Processed Video Path: {video_path}")
            st.session_state.video_path=video_path
            yvu.rename_files(temp_dir)
            # Upload the processed file to Dataiku
            # di.upload_files(video_path)

            # Store success message in Streamlit session state
            st.session_state.uploaded = "File uploaded successfully!"
                # st.success(st.session_state.uploaded)
            # st.success(f"Received YouTube link: {youtube_link}")
            # video_path = yvu.download_youtube_video(youtube_link, inp.youtube_download_folder)
            # video_path = yvu.rename_video_path(video_path)
            # print(video_path)
            # yvu.rename_files(inp.youtube_download_folder)
            # di.upload_files(video_path)
            # st.session_state.uploaded="Files uploaded to Dataiku successfully!"
            # st.success(st.session_state.uploaded)

    # st.session_state.url=st.text_input("",placeholder="Enter the link or file path")


    cols=st.columns([0.1,0.1,0.8],vertical_alignment='center')

    chat_container = st.container()
    with cols[0]:
        placeholder_button=st.empty() 
        # placeholder_download=st.empty()       
        if st.session_state.uploaded: 
            # st.button("Start Processing", on_click=process)
            st.session_state.upload_button=False
            placeholder_button.button("Start Processing", on_click=process)
        else: 
            placeholder_button.button("Upload",on_click=upload_button)

    
    with cols[2]:
        placeholder=st.empty()
        if st.session_state.uploaded:
            placeholder.success(st.session_state.uploaded)
        if st.session_state.process==True:
            # st.write(st.session_state.uploaded)
            if st.session_state.uploaded:
                with st.spinner("In Progress"):   
                    # st.session_state.clean_transcript = di.clean_transcript()
                    st.session_state.clean_transcript = trans.transcription(st.session_state.video_path)

                # if st.session_state.clean_transcript:
                #     placeholder_button.download_button("Download Cleaned Transcript",st.session_state.clean_transcript, file_name="Clean_Transcript.txt", mime="text/plain")
                placeholder.success("✅ All set! The video has been successfully transcribed, and your Q&A is ready to explore. Dive in and ask away!")
                st.session_state.starter_question_display="Yes"
                # with chat_container:
                #     st.markdown('<div class="starter-questions-header">Examples</div>',unsafe_allow_html=True)
                #     starter_qna_cols = st.columns([0.5, 0.5],vertical_alignment='center')
                #     with starter_qna_cols[0]:
                #         st.button("Give me a one page summary on the shared content",on_click=q1,type='primary',use_container_width=True)
                #     with starter_qna_cols[1]:
                #         st.button("Provide detailed notes for the content shared above.",on_click=q2,type='primary',use_container_width=True)                
            else:    
                placeholder.warning("Please enter the Url or Upload the files")
            st.session_state.process=False  
        
    with cols[1]:   
        placeholder_download=st.empty() 
        if st.session_state.clean_transcript:
            # placeholder_button.download_button("Download Transcript",st.session_state.clean_transcript, file_name="Clean_Transcript.txt", mime="text/plain")
            # st.session_state.upload_button=False
            # st.session_state.uploaded=None
            placeholder_download.download_button("Download Transcript",st.session_state.clean_transcript, file_name="Clean_Transcript.txt", mime="text/plain")
        # st.write(f"value {st.session_state.starter_question_display}")
        if st.session_state.starter_question_display=="Yes":
            with chat_container:
                st.markdown('<div class="starter-questions-header">Examples</div>',unsafe_allow_html=True)
                starter_qna_cols = st.columns([0.5, 0.5],vertical_alignment='center')
                with starter_qna_cols[0]:
                    st.button("Give me a one page summary on the shared content",on_click=q1,type='primary',use_container_width=True)
                with starter_qna_cols[1]:
                    st.button("Provide detailed notes for the content shared above.",on_click=q2,type='primary',use_container_width=True)                


    if st.session_state.welcome_message==True:
        with chat_container:
            chat_container.markdown(f"<div class='welcome-message'> Hello, Vivek </div>", unsafe_allow_html=True)
            st.session_state.welcome_message = False        

    # Chat Input Section
    if question := st.chat_input("Ask Me Anything") or st.session_state.starter_question:
        st.session_state.starter_question_display="No"
        st.session_state.starter_question=False
        # st.write(st.session_state.starter_question_display)
        placeholder.empty()
        # if uploaded_transcript:    
        with chat_container:
            # Display previous chat messages
            for i, entry in enumerate(st.session_state.hist_list):
                if i % 2 == 0:
                # if i % 2 != 0:
                    chat_container.chat_message("user",avatar=avatars["user"]).markdown(
                        entry, unsafe_allow_html=True)
                else:
                    chat_container.chat_message("assistant",avatar=avatars["assistant"]).markdown(
                        entry,unsafe_allow_html=True)

            # Display the new user question
            chat_container.chat_message("user",avatar=avatars["user"]).markdown(
                question,unsafe_allow_html=True)

            # Get the assistant's response
            answer = qna.get_answer(question, st.session_state.hist, st.session_state.clean_transcript)

            # Display the assistant's response
            chat_container.chat_message("assistant",avatar=avatars["assistant"]).markdown(
                answer,unsafe_allow_html=True)

        # Update chat history
        st.session_state.hist_list.append(question)
        st.session_state.hist_list.append(answer)

        # Keep the last 5 interactions in the history
        st.session_state.hist = "\n\n".join(st.session_state.hist_list[-5:])
        # else:
        #     st.warning("Please upload transcript first")

