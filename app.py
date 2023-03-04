import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Analyze your Chats '\n' upload .txt file of chats without media")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()

    # to convert byte data into string of utf-8
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)

    #fetching unique users from the dataframe['user]
    userlist=df['user'].unique().tolist()

    #now we need to remove the names groupnotification and 
    #also sort in ascending order
    userlist.remove('groupnotification')
    userlist.sort()
    userlist.insert(0,'Overall')
    selecteduser=st.sidebar.selectbox("Show analysis wrt",userlist)
    #Overall will be at first for--group level analysis
    if st.sidebar.button("Show Analysis"):
        nummessages,words,nummedia,numlink=helper.fetch_stats(selecteduser,df)
        st.title('Top Statistics')
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(nummessages)
        with col2:
            st.header("Total Words")
            st.title(words) 
        with col3:
            st.header("Media Shared")
            st.title(nummedia) 
        with col4:
            st.header("Links Shared")
            st.title(numlink) 
        #monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selecteduser,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        dailytimeline=helper.dailytimeline(selecteduser,df)
        fig,ax=plt.subplots()
        ax.plot(dailytimeline['onlydate'],dailytimeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Actiivty MAp
        col1,col2=st.columns(2)

        with col1:
            st.title("Most busy day")
            busyday=helper.weekactivitymap(selecteduser,df)
            fig,ax = plt.subplots()
            plt.figure(figsize=(25,10))
            plt.xticks(rotation='vertical')
            ax.bar(busyday.index,busyday.values)
            st.pyplot(fig)

        with col2:
            st.title("Most busy month")
            busymonth=helper.monthactivitymap(selecteduser,df)
            fig,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busymonth.index,busymonth.values,color='yellow')
            st.pyplot(fig)
        
        st.title("Weekly Activity Map")
        userheatmap=helper.activityheatmap(selecteduser,df)
        fig,ax =plt.subplots()
        plt.xticks(rotation='vertical')
        ax=sns.heatmap(userheatmap)
        st.pyplot(fig)


    #finding the busiest user in the group
        if selecteduser=='Overall':
           st.title('Most Busy Users')
           x,busydf=helper.mostbusyusers(df)
           fig,ax=plt.subplots()
           col1,col2=st.columns(2) 

           with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
           with col2:
                st.dataframe(busydf)

        #Wordcloud Formation
        st.title("WordCloud")
        dfwc=helper.createwordcloud(selecteduser,df)
        fig,ax=plt.subplots()
        ax.imshow(dfwc)
        st.pyplot(fig)

        #Most common words
        st.title("Most Common Words")
        mostcommonworddf=helper.mostcommonwords(selecteduser,df)
        fig,ax=plt.subplots()
        ax.barh(mostcommonworddf[0],mostcommonworddf[1])
        st.pyplot(fig)
        plt.xticks(rotation='vertical')
        # st.dataframe(mostcommonworddf)
        
        #Emoji Analysis
        emojidf=helper.emojihelper(selecteduser,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emojidf)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emojidf[1].head(),labels=emojidf[0].head(),autopct="%0.2f")
            st.pyplot(fig)
    



    