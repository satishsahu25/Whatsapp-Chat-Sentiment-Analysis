import re
import pandas as pd

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2},\s\d{1}:\d{2}\spm\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    for i in range(0,len(dates)):
        dates[i]=dates[i][0:9]+" "+str(int(dates[i][10])+12)+dates[i][11:14]
    df=pd.DataFrame({'usermessage':messages,'messagedate':dates})
    df.rename(columns={'messagedate':'date'},inplace=True)
    df['date']=pd.to_datetime(df['date'])
    users=[]
    messages=[]
    for message in df['usermessage']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]: #user name
            users.append(entry[1])
            messages.append(entry[2])
        else: #if no username then its group notifcation
            users.append('groupnotification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['usermessage'],inplace=True)
    df['year']=df['date'].dt.year
    df['onlydate']=df['date'].dt.date
    df['dayname']=df['date'].dt.day_name()
    df['month']=df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    period=[]

    for hour in df[['dayname','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str("00"))
        elif hour==0:
            period.append(str("00")+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
            
    df['period']=period

    return df