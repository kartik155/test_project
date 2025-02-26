import os
import Clean_Transcript as ct
import Quote_bank as qb
import streamlit as st

st.set_page_config(page_title="HawkAI", page_icon="images/Beghou_logo.png", layout="wide")


    
# # Replace selectbox with radio button
page = st.sidebar.radio("", ["Transcription", "Quote Bank"])

if page == "Transcription":
    ct.Clean_Transcript()
elif page == "Quote Bank":
    qb.Quote_Bank()

    
