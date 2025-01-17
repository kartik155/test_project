import streamlit as st
import QnA_model as qna
import os


avatars = {
    "assistant" : "images/gemini-logo.svg",
    "user": "images/VG.png"
}

# Page Configurations
st.set_page_config(page_title="HawkAI", page_icon="images/gemini-logo.svg", layout="wide")

# Custom CSS for styling
st.markdown(""" 
    <style>
        /* Title Styling */
        .markdown-header {
            color:#3184a0; 
            font-weight: bold;
            font-size: 50px;
            margin-left: 170px;
            /*padding: 15px;*/
            border-radius: 10px;
            text-align: left
                        }
        /* Welcome Message */
        .welcome-message {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px; /* Adjust height to the container's height */
            font-size: 50px;
            font-weight: bold;
            color: #D36474; 
           text-align: center;
            margin-top: 50px; /* Optional: Adds spacing above */
        }
        /* Chat Message Styling */
        .chat-message {             
            display:block; /* Use block for better alignment */
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
            max-width: 70%;
            word-wrap: break-word;
            position: relative; /* Position relative to align the color properly */
            width: fit-content;
        }

        /* User Message - Right Aligned */
        .chat-message.user {
            background-color: #E9EEF6;
            font-size: 18px;
            margin-left: auto;
            margin-right: 0;
            text-align: right;
            border-radius: 8px; /* Rounded corners for the user messages */
            padding-right: 15px; /* Extra padding for the message */
            /*max-width: 85%;  /* Set a max width so the text doesn't overflow */ */
        }

        /* Assistant Message - Left Aligned */
        .chat-message.assistant {
            font-size: 18px;
            margin-right: auto;
            margin-left: 0;
            text-align: left;
            border-radius: 8px;
          /*  max-width: 85%; /* Set a max width to keep things balanced */ */
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

def clear_chat_history():
    st.session_state.hist_list = []
    st.session_state.hist = ""

# if 'clicked' not in st.session_state:
#     st.session_state.clicked = False

# def set_clicked():
#     st.session_state.clicked = True

# st.button('Upload File', on_click=set_clicked)

# Sidebar Configuration
with st.sidebar:
    # st.image('BGNE_BIG.svg', use_container_width=True)
    clean_transcript = ""
    # if st.session_state.clicked:    
    with st.expander("Upload file"):
        uploaded_transcript = st.file_uploader(
        "Upload your transcript here", type=['txt', 'docx'], key="Transcript_Upload", label_visibility="collapsed")
            
        if uploaded_transcript:
            bytes_data = uploaded_transcript.read()
            file_name = os.path.join("./", uploaded_transcript.name)
            with open(file_name, "r", encoding="utf-8") as file:
                clean_transcript = file.read()
            st.success("✅ Transcript uploaded successfully")
            st.session_state.transcript = "completed"

    st.sidebar.button("Clear Chat History", on_click=clear_chat_history)
st.image('images/BGNE_BIG.svg', width=200)

# cols= st.columns([0.2,0.8])
# with cols[0]:
#     st.image('BGNE_BIG.svg', width=200)
# with cols[1]:
    # Title Section
    # st.markdown("<div class='markdown-header'> Chat with HawkAI</div>", unsafe_allow_html=True)

# Tabs for Chat and Transcript
tabs = st.tabs(["Chat", "Transcript"])

with tabs[1]:
    if st.session_state.transcript == "completed":
        st.write(clean_transcript, wrap_lines=True)
    else:
        st.info("🔄 No transcript available yet.")

with tabs[0]:
    chat_container = st.container()
    
    if st.session_state.welcome_message==True:
        with chat_container:
            chat_container.markdown("<div class='welcome-message'> Hello, ViveK </div>", unsafe_allow_html=True)
            
            st.session_state.welcome_message = False

# Chat Input Section
if question := st.chat_input("Ask HawkAI"):
    if uploaded_transcript:    
        with chat_container:
            # Display previous chat messages
            for i, entry in enumerate(st.session_state.hist_list):
                if i % 2 == 0:
                    chat_container.chat_message("user",avatar=avatars["user"]).markdown(
                        entry, unsafe_allow_html=True)
                else:
                    chat_container.chat_message("assistant",avatar=avatars["assistant"]).markdown(
                        entry,unsafe_allow_html=True)

            # Display the new user question
            chat_container.chat_message("user",avatar=avatars["user"]).markdown(
                question,unsafe_allow_html=True)

            # Get the assistant's response
            answer = qna.get_answer(question, st.session_state.hist, clean_transcript)

            # Display the assistant's response
            chat_container.chat_message("assistant",avatar=avatars["assistant"]).markdown(
                answer,unsafe_allow_html=True)

        # Update chat history
        st.session_state.hist_list.append(question)
        st.session_state.hist_list.append(answer)

        # Keep the last 5 interactions in the history
        st.session_state.hist = "\n\n".join(st.session_state.hist_list[-5:])
    else:
        st.warning("Please upload the transcript")

