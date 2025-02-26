import streamlit as st
import dataikuapi
import os.path
import pandas as pd
import io #to keep the data in the strcutured format 
import os
import tempfile
import dataiku as di

def Quote_Bank():
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)

    open_api_key= os.getenv("OPENAI_API_KEY")
    dataiku_url=os.getenv("DATAIKU_URL")
    dataiku_api_key = os.getenv("DATAIKU_API_KEY")

    # client = dataikuapi.DSSClient(dataiku_url, dataiku_api_key,no_check_certificate=True)
    # project = client.get_project("HAWKAI")

    # st.set_page_config(page_title="Quote Bank", page_icon="gemini_avatar.png", layout="wide",initial_sidebar_state="collapsed")

    st.session_state.transcript = None
    st.session_state.hist_list = []
    st.session_state.hist = ""
    st.session_state.welcome_message = True
    st.session_state.chat_history = True
    st.session_state.process = False
    st.session_state.uploaded = None
    st.session_state.starter_question = None
    st.session_state.starter_question_display = "No"
    st.session_state.clean_transcript = None
    st.session_state.upload = None
    st.session_state.upload_button = False
    st.session_state.upload_option = False

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
    st.markdown(""" 
        <style>
            .header-title {
            font-size: 40px;
            font-weight: bold;
            color: #2B7795;
            text-align: left;
            margin-bottom: 10px;
            margin-top: 5px
            }
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
    main_cols = st.columns(8)
    with main_cols[0]:
        st.write("")
        st.image('Header_logo.png', width=150)

    with main_cols[7]:
        st.write("")
        st.write("")
        st.image("BGNE_BIG.svg", width=150)
    # st.markdown("<div class=header-title> Quote Bank Creation </div>",unsafe_allow_html=True)
    # st.title("Quote Bank Creation")
    # file_name=di.get_filename()
    # selected_name = st.selectbox("Select File name to process for Quote bank:", file_name)

    if 'quote_bank' not in st.session_state:
        st.session_state.quote_bank = False

    with st.form(key='event_form'):
        st.markdown("<div class=header-title>Quote Bank Form</div>", unsafe_allow_html=True)
        

        col1, col2 = st.columns([1, 2])  # Left side input, right side output
        
        with col1:
            date = st.date_input("Date")        
            partner_name = st.text_input("Partner Name", "Targeted Oncology")        
            team = st.text_input("Team", "Marketing")
            location = st.text_input("Location", "Virtual (Maryland + Virginia)")            
                
        with col2:
            event_name = st.text_input("Event Name", "Virtual Case Based RoundTable - Updates in Treatment of CLL")
            event_type = st.text_input("Event Type", "Case Based RoundTable")
            virtual_in_person = st.text_input("Virtual/In-Person", "Virtual")

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            formatted_date = date.strftime("%m/%d/%Y")
            formatted_output = (f"Date: {formatted_date}\n"
                                f"Event Name: {event_name}\n"
                                f"Partner Name: {partner_name}\n"
                                f"Event Type: {event_type}\n"
                                f"Team: {team}\n"
                                f"Virtual/In-Person: {virtual_in_person}\n"
                                f"Location: {location}")    
            # st.text_area("Formatted Output", formatted_output, height=150)
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, "readme.txt")
                with open(file_path, "w") as file:
                    file.write(formatted_output)                
                # di.upload_files(file_path)
                st.success("Form submitted successfully")
                # st.success(f"File saved at: {file_path}")
                st.session_state.quote_bank=True
    if st.session_state.quote_bank==True:
        if st.button("Genreate Quote Bank"):
            # df=di.quote_bank()
            # st.success("Quote bank generated successfully")
            # st.data_editor(df)

                
