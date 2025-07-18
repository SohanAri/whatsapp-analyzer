from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    num_media = len(df[df['message']=='<Media omitted>\n'])
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_link = len(links)
    return num_messages, num_words, num_media, num_link

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
    mdf=ndf[ndf['user']!='notification']
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
    df = df[df['user']!='notification']
    #remove stop words
    words=[]
    for messages in df['message']:
        for word in messages.lower().split():
             if word not in stop_words:
                 words.append(word)
    rdf = pd.DataFrame(Counter(words).most_common(20))
    return rdf
