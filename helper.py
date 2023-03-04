from urlextract import URLExtract
extract=URLExtract()
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji

def fetch_stats(selecteduser,df):

    if selecteduser!='Overall': #overall group ke kitne messages hai
        df=df[df['user']==selecteduser]
    #1. no of messages
    nummessages=df.shape[0]
    #2. no  of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
    #3. no  of media files
    nummedia=df[df['message']=='<Media omitted>\n'].shape[0]
    #4. no. of links shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    numlink=len(links)



    return nummessages,len(words),nummedia,numlink

def mostbusyusers(df):
    x=df['user'].value_counts().head()
    #percentage of user's message
    busydf=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,busydf

def createwordcloud(selecteduser,df):

    f=open('stop_hinglish.txt','r')
    stopwords=f.read()

    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]

    tempdf=df[df['user']!='groupnotification']
    temp=tempdf[tempdf['message']!='<Media omitted>\n']

    #removing all stop words
    def removestopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
        #forming again sentence and sending it

    
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    #applying the function
    temp['message']=temp['message'].apply(removestopwords)
    dfwc=wc.generate(temp['message'].str.cat(sep=" "))
    return dfwc


def mostcommonwords(selecteduser,df):
    f=open('stop_hinglish.txt','r')
    stopwords=f.read()

    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]

    tempdf=df[df['user']!='groupnotification']
    temp=tempdf[tempdf['message']!='<Media omitted>\n']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
        #checking that it should not be present in stopwords
            if word not in stopwords:
                words.append(word)
        

    mostcommonworddf=pd.DataFrame(Counter(words).most_common(20))
    return mostcommonworddf

def emojihelper(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]
    emojis=[]
    for message in df['message']:
        emojis.extend(emoji.distinct_emoji_list(message))
    emojidf=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojidf


def monthly_timeline(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time']=time
    
    return timeline



def dailytimeline(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]
    dailytimeline=df.groupby('onlydate').count()['message'].reset_index()

    return dailytimeline
    

def weekactivitymap(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]

    return df['dayname'].value_counts()


def monthactivitymap(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]
    
    return df['month'].value_counts()

def activityheatmap(selecteduser,df):
    if selecteduser!='Overall':
        df=df[df['user']==selecteduser]
    userheatmap=df.pivot_table(index='dayname',columns='period',values='message',aggfunc='count').fillna(0)

    return userheatmap