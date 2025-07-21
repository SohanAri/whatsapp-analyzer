import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import helper
import preprocessor
from helper import most_busy_users
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


        selected_user = st.sidebar.selectbox("Show analysis wrt ",user_list)
        most_busy_users(df)
        if st.sidebar.button("Show Analysis"):
            num_messages,num_words,num_media,num_link = helper.fetch_stats(selected_user, df)
            col1,col2,col3,col4 =st.columns(4)
            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total words")
                st.title(num_words)
            with col3:
                st.header("Total Media")
                st.title(num_media)
            with col4:
                st.header("Total links")
                st.title(num_link)

        if selected_user == 'Overall':
            st.title("Most Busy Users")
            # Assume helper.most_busy_users(df) returns a Pandas Series (value_counts)
            x = helper.most_busy_users(df)

            # Create a new DataFrame for showing percentages
            percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
            percent_df.columns = ['User', 'Message Percentage']

            col1, col2 = st.columns(2)

            with col1:
                st.header("Most Active Users (Bar Chart)")
                fig, ax = plt.subplots() #creating a library of plots

                ax.bar(x.index, x.values, color='skyblue')
                plt.xticks(rotation='vertical')  # Rotate labels for better readability

                # --- FIX 2: Use st.pyplot() to display a Matplotlib figure ---
                st.pyplot(fig)

            with col2:
                st.header("User Activity (Data)")
                st.dataframe(percent_df)

        df_wc = helper.create_word_cloud(selected_user, df)
        plt.imshow(df_wc)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis('off') # This hides the x and y axis labels
        st.title("Word Cloud")
        st.pyplot(fig)
        #most common words
        most_common_df =helper.most_common_words(selected_user, df)
        st.title("Most Common Words")
        # now i want to show a bar graph
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='green')
        ax.set_xlabel("Counter")
        ax.set_ylabel("Words")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #st.dataframe(most_common_df)

        # months trends
        mf= helper.month_trends(selected_user,df)
        st.title("Monthly Trends")
        if selected_user == 'Overall':
            st.header("Monthly User Activity")
            fig, ax = plt.subplots()

            # Use the DataFrame's plot method and tell it to draw on your Matplotlib axes
            mf.plot(kind='line', ax=ax)

            # Now you can customize the Matplotlib plot
            ax.set_xlabel("Month")
            ax.set_ylabel("Number of Messages")
            ax.legend(title='User')
            plt.xticks(rotation='vertical')

            # Display the Matplotlib figure in Streamlit
            st.pyplot(fig)
        else:
            mmf = helper.month_trends("Overall",df)
            col1,col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.set_xlabel("Months")
                ax.set_ylabel("Messages")
                ax.bar(mf['month'], mf['messages'], color='blue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                fig, ax = plt.subplots()

                # Use the DataFrame's plot method and tell it to draw on your Matplotlib axes
                mf.plot(kind='line', ax=ax)

                # Now you can customize the Matplotlib plot
                ax.set_xlabel("Month")
                ax.set_ylabel("Number of Messages")
                ax.legend(title='User')
                plt.xticks(rotation='vertical')

                # Display the Matplotlib figure in Streamlit
                st.pyplot(fig)
        #emojis
        ef = helper.emojis_anal(selected_user,df)
        st.title("Emoji Analsis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(ef)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(ef[1].head(10),labels=ef[0].head(10),autopct='%1.1f%%')
            st.pyplot(fig)





