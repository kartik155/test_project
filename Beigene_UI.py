import os
import Clean_Transcript as ct
import Quote_bank as qb
import streamlit as st

st.set_page_config(page_title="HawkAI", page_icon="Beghou_logo.png", layout="wide", initial_sidebar_state='collapsed')


    
# # Replace selectbox with radio button
page = st.sidebar.radio("", ["Transcription", "Quote Bank"])

if page == "Transcription":
    ct.Clean_Transcript()
elif page == "Quote Bank":
    qb.Quote_Bank()








##############################################################################################################################################################################################################
# import streamlit as st
# import QnA_model as qna
# import os
# import tempfile
# import base64
# import time
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader


# avatars = {
#     "assistant" : "gemini-logo.svg",
#     "user": "VG.png"
# }

# # Page Configurations
# st.set_page_config(page_title="HawkAI", page_icon="gemini_avatar.png", layout="wide",initial_sidebar_state="collapsed")
# # st.logo('BGNE_BIG.svg')

# # def get_image_as_base64(file_path):
# #     """
# #     Convert an image file to a base64-encoded string.
# #     """
# #     with open(file_path, "rb") as f:
# #         data = f.read()
# #     return base64.b64encode(data).decode()


# # Load the image and encode it to base64
# # image_file = "HawkAI_Logo_CenturyItalic.png"
# # base64_img = get_image_as_base64(image_file)

# # # Define background image styling
# # logo_file="logo.png"
# # logo=get_image_as_base64(logo_file)
# # # Define background image styling
# # header_logo_file="Header_logo.png"
# # header_logo=get_image_as_base64(header_logo_file)

# # st.image(logo_file)

# # from yaml.loader import SafeLoader
# # with open('.streamlit/config.yaml') as file:
# #     config = yaml.load(file, Loader=SafeLoader)

# # authenticator = stauth.Authenticate(
# #     config['credentials'],
# #     config['cookie']['name'],
# #     config['cookie']['key'],
# #     config['cookie']['expiry_days'],
# # )

# custom_css=f"""
# <style>
# [data-testid="stMainBlockContainer"] {{
#     width: 100%;
#     padding: 2rem 1rem 5rem;

# }}

# [data-testid="stBottomBlockContainer"] 
# {{
#     width: 100%;
#     padding: 0rem 1rem 4rem;
# }}
# </style>
# """

# st.markdown(custom_css,unsafe_allow_html=True)

# main_cols = st.columns(8)
# with main_cols[0]:
#     st.image('Header_logo.png', width=150)

# with main_cols[7]:
#     st.write("")
#     st.write("")
#     st.write("")
#     st.image("BGNE_BIG.svg", width=150)

# # st.image("Header_logo.png",width=150)

# # authenticator.login()
# # name, authentication_status, username = authenticator.login('Login', location='main')




# # if st.session_state['authentication_status']:
#     # Custom CSS for styling
# st.markdown(""" 
#     <style>
#         /* Welcome Message */
#         .welcome-message {
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             height: 200px; /* Adjust height to the container's height */
#             font-size: 50px;
#             font-weight: bold;
#             color: #2B7795; 
#         text-align: center;
#             margin-top: 50px; /* Optional: Adds spacing above */
#         }
#         .header{
#             vertical-align: text-top;
#             }
#         /* Url Input */
#         .stTextInput {
#             background: #f3f2f0;
#             /*border-radius: 10px;*/
#         /* padding: 8px; */
#             /*border: 2px solid #2B7795;*/
#         }
#         /* Primary Buttons */
#         button[kind="primary"] {
#             background-color: transparent;
#             border: 2px solid #2B7795; 
#             color: #2B7795; 
#             font-size:
#             padding: 16px 40px;
#             border-radius: 8px;
#             cursor: pointer;
#             height: 48px; 
#         }

#         button[kind="primary"]:hover {
#             background-color: #15396F;
#             color: white;
#             border-color: #15396F;
#         }    
        
#         /* Buttons */
#         button[kind="secondary"] {
#             background-color: #2B7795;
#             border: none;
#             color: white;
#             font-size: 16px;
#             padding: 8px 20px;
#             border-radius: 8px;
#             cursor: pointer;
#             height: 48px;
#         }
#         button[kind="secondary"]:hover {
#             background-color: #15396F;
#             color: white;
#         }
#                     .starter-questions-header {
#         font-size: 24px;
#         font-weight: bold;
#         color: #2B7795; /* Set the color */
#         text-align: center; /* Center the text */
#         text-transform: uppercase; /* Transform text to uppercase */    
#         position: relative; /* Positioning for pseudo-elements */
#     }
    
#     .starter-questions-header::before, .starter-questions-header::after {
#         content: "";
#         position: absolute;
#         top: 50%;
#         transform: translateY(-50%); /* Ensure proper vertical alignment */    
#         width: calc(50% - 80px); /* Dynamic length relative to the text */
#         border-bottom: 2px solid #2B7795; /* Line color */
#         display: inline-block;
#     }

#     .starter-questions-header::before {
#         left: 0;
#     }

#     .starter-questions-header::after {
#         right: 0;
#     }    
# </style>
# """, unsafe_allow_html=True)


# if 'transcript' not in st.session_state:
#     st.session_state.transcript = None

# # Initialize Session State for Chat History
# if 'hist_list' not in st.session_state:
#     st.session_state.hist_list = []
# if 'hist' not in st.session_state:
#     st.session_state.hist = ""

# if 'welcome_message' not in st.session_state:
#     st.session_state.welcome_message = True

# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = True
# if 'process' not in st.session_state:
#     st.session_state.process=False
# if 'url' not in st.session_state:
#     st.session_state.url=None
# if 'starter_question' not in st.session_state:
#     st.session_state.starter_question=None

# def clear_chat_history():
#     st.session_state.hist_list = []
#     st.session_state.hist = ""

# def process():
#     st.session_state.process = True
#     st.session_state.hist_list = []
#     st.session_state.hist = ""

# def q1():
#     st.session_state.starter_question="Give me a one page summary on the shared content"
# def q2():
#     st.session_state.starter_question="Provide detailed notes for the content shared above"

# # Sidebar Configuration
# with st.sidebar:
#     # st.write(f'Welcome *{st.session_state["name"]}*')
#     # authenticator.logout()
#     # st.image('BGNE_BIG.svg', use_container_width=True)
#     clean_transcript = ""
#     # if st.session_state.clicked:    
#     with st.expander("Upload your file"):
#         uploaded_transcript = st.file_uploader(
#         "Upload your transcript here", type=['txt', 'docx'], key="Transcript_Upload", label_visibility="collapsed")
            
#         if uploaded_transcript:
#             # bytes_data = uploaded_transcript.read()
#             # file_name = os.path.join("./", uploaded_transcript.name)
#             # with open(file_name, "r", encoding="utf-8") as file:
#             #     clean_transcript = file.read()

#             clean_transcript = uploaded_transcript.read()
        
#             st.success("✅ Transcript uploaded successfully")
#             st.session_state.transcript = "completed"
#         else:
#                 clean_transcript = None
#     st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

# # st.image('BGNE_BIG.svg', width=200)    
# # st.image("Header_logo.png",width=150)
# # st.markdown(" ### Enter the Youtube Link:")



# # Additional logic remains unchanged

# # h_cols=st.columns([0.03,0.97])
# # with h_cols[0]:
# #     # st.write("")
# #     st.image("youtube-icon.svg",width=5,use_container_width=True)
# # with h_cols[1]:
# #     st.write("")
# #     st.markdown("<div class='header'> Enter the Youtube Link </div>",unsafe_allow_html=True)
# st.session_state.url=st.text_input("",placeholder="Enter the link or file path")


# # Custom Text Input with Icon


# cols=st.columns([0.2,0.8],vertical_alignment='center')

# chat_container = st.container()
# with cols[0]:
#     st.button("Start Processing", on_click=process)
        

# with cols[1]:
#     placeholer=st.empty()
#     if st.session_state.process==True:
#         if st.session_state.url:
#             with st.spinner("In Progress"):
#                 time.sleep(5)    
#             placeholer.success("✅ All set! The video has been successfully transcribed, and your Q&A is ready to explore. Dive in and ask away!")
#             with chat_container:
#                 st.markdown('<div class="starter-questions-header">Examples</div>',unsafe_allow_html=True)
#                 starter_qna_cols = st.columns([0.5, 0.5],vertical_alignment='center')
#                 with starter_qna_cols[0]:
#                     st.button("Give me a one page summary on the shared content",on_click=q1,type='primary',use_container_width=True)
#                 with starter_qna_cols[1]:
#                     st.button("Provide detailed notes for the content shared above.",on_click=q2,type='primary',use_container_width=True)
#             # placeholer.success("✅ Process is completed")
#             # Intro="Hey there! I am HawkAI - Your assistant for today. The video is all transcribed and ready. How can I assist you today? "
            
#             # chat_container.chat_message("assitant",avatar=avatars["assistant"]).markdown(
#             #         Intro, unsafe_allow_html=True)
#             # st.session_state.hist_list.append(Intro)
#         else:    
#             placeholer.warning("Please enter the Url")
#         st.session_state.process=False    

# if st.session_state.welcome_message==True:
#     with chat_container:
#         # Name=st.session_state["name"]
#         # chat_container.markdown(f"<div class='welcome-message'> Hello, {Name} </div>", unsafe_allow_html=True)
#         chat_container.markdown(f"<div class='welcome-message'> Hello, Vivek </div>", unsafe_allow_html=True)
        
#         st.session_state.welcome_message = False        

# # Chat Input Section
# if question := st.chat_input("Ask Me Anything") or st.session_state.starter_question:
#     st.session_state.starter_question=False
#     placeholer.empty()
#     # if uploaded_transcript:    
#     with chat_container:
#         # Display previous chat messages
#         for i, entry in enumerate(st.session_state.hist_list):
#             if i % 2 == 0:
#             # if i % 2 != 0:
#                 chat_container.chat_message("user",avatar=avatars["user"]).markdown(
#                     entry, unsafe_allow_html=True)
#             else:
#                 chat_container.chat_message("assistant",avatar=avatars["assistant"]).markdown(
#                     entry,unsafe_allow_html=True)

#         # Display the new user question
#         chat_container.chat_message("user",avatar=avatars["user"]).markdown(
#             question,unsafe_allow_html=True)

#         # Get the assistant's response
#         answer = qna.get_answer(question, st.session_state.hist, clean_transcript)

#         # Display the assistant's response
#         chat_container.chat_message("assistant",avatar=avatars["assistant"]).markdown(
#             answer,unsafe_allow_html=True)

#     # Update chat history
#     st.session_state.hist_list.append(question)
#     st.session_state.hist_list.append(answer)

#     # Keep the last 5 interactions in the history
#     st.session_state.hist = "\n\n".join(st.session_state.hist_list[-5:])
#     # else:
#     #     st.warning("Please upload transcript first")

# # elif st.session_state['authentication_status'] is False:
# # st.error('Username/password is incorrect')
# # elif st.session_state['authentication_status'] is None:
# # st.write("")
# # st.warning('Please enter your username and password')
# # authenticator.logout('Logout', 'main')
