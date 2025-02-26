import os
import Clean_Transcript as ct
import Quote_bank as qb
import streamlit as st

st.set_page_config(page_title="HawkAI", page_icon="images/Beghou_logo.png", layout="wide")


    
# # Replace selectbox with radio button
page = st.sidebar.radio("", ["Transcript", "Quote Bank"])

if page == "Transcript":
    ct.Clean_Transcript()
elif page == "Quote Bank":
    qb.Quote_Bank()

    