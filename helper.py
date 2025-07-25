from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    dmc = 0
    dme = 0
    for message in df['message']:
        if 'This message was deleted' in message:
            dmc=dmc+1
        elif '<This message was edited>' in message:
            dme = dme+1
        words.extend(message.split())
    num_words = len(words)
    num_media = len(df[df['message']=='<Media omitted>\n'])
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_link = len(links)
    return num_messages, num_words, num_media, num_link, dmc, dme

def most_busy_users(df):
    if len(df['user'].unique()) ==2 :
        x = df['user'].value_counts().head(2)
        return x
    else:
        x = df['user'].value_counts().head(4)
        return x

def create_word_cloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    ndf=df[df['message']!='<Media omitted>\n']
    mdf=ndf[ndf['user']!='group_notification']
    wc = WordCloud(width = 800, height = 800, background_color = 'white')
    df_wc = wc.generate(mdf['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stopWords.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    #remove the media omitted data
    df = df[df['message']!='<Media omitted>\n']
    #remove the group notifications
    df = df[df['user']!='group_notification']
    #remove stop words
    words=[]
    for messages in df['message']:
        for word in messages.lower().split():
             if word not in stop_words:
                 words.append(word)
    rdf = pd.DataFrame(Counter(words).most_common(20))
    return rdf

def month_trends(selected_user,df):
    if selected_user == 'Overall':
        df = df[df['user'] != 'group_notification']
        users = df['user'].unique()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

        # 1. Create a dictionary to hold all the data
        user_activity_data = {'Month': months}

        # 2. Loop through each user and add their message counts to the dictionary
        for user in users:
            messages = []
            for month in months:
                # Count messages for the specific user in the specific month
                num_msg = len(df[(df['user'] == user) & (df['month'] == month)])
                messages.append(num_msg)

            # Use the user's name as the key for their message list
            user_activity_data[user] = messages

        # 3. Create the DataFrame from the complete dictionary
        mf = pd.DataFrame(user_activity_data)
        mf.set_index('Month', inplace=True)

        #print(mf)
        return mf

    else :
        df = df[df['user'] == selected_user]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    messages=[]
    for month in months:
        num_msg = len(df[df['month']==month])
        messages.append(num_msg)
    comb = list(zip(months, messages))
    mf = pd.DataFrame(comb,columns=['month','messages'])
    #print(mf)
    return mf

def emojis_anal(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['month_num'] = df['date'].dt.month_name()
    tf = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []

    for i in range(tf.shape[0]):
        exp = tf['month'][i] + '-' + str(tf['year'][i])
        time.append(exp)
    tf['time'] = time
    return tf

def dating(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['only_date']= df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

