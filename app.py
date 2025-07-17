import streamlit as st
import pandas as pd
import preprocessor

st.sidebar.title('Whatsapp Chat Analyzer')

# In your main Streamlit app file

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # You can comment this out now that you know it works
    # st.text(data)

    df = preprocessor.preprocess(data)

    # --- Add this check ---
    if df.empty:
        st.warning("The processed DataFrame is empty.")
        st.info(
            "This can happen if the date and time format in your chat file doesn't match the regex pattern in your preprocessor.py file. No messages were successfully parsed.")
    else:
        st.dataframe(df)
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.insert(0,'Overall')
        st.sidebar.selectbox("Show analysis wrt ",user_list)
        if st.sidebar.button("Show Analysis"):
            pass