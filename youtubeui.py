import streamlit as st
import pickle
import pandas as pd
import mysql.connector
conn = mysql.connector.connect(
host = "127.0.0.1",
port = "3306",  #mysqlconnector,commas,not changing into dataframe,tablename variable error,
database = "youtube",
username = "root",
password = "naandhaan"
)
cursor = conn.cursor()
cursor.execute('select * from youtube')
total1 = cursor.fetchall()
cursor.execute('SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = "youtube" AND TABLE_SCHEMA = "youtube" ORDER BY ORDINAL_POSITION')
a = cursor.fetchall()
total = pd.DataFrame(total1)
flat = [i[0] for i in a]
total.columns = flat
with open ('model.pkl','rb') as f:
    K = pickle.load(f)
with open ('Transform.pkl','rb') as f:
    tf = pickle.load(f)
def videos(a):
    b = tf.transform([a])
    c = K.predict(b)[0]
    tt = total[total['cluster'] == c]
    return tt
a = st.text_input('Youtube Search:')
h = videos(a)

#if a:
h = h.sort_values(by = 'statistics.likeCount',ascending = False)
for i,j in h.iterrows():

    col1,col2=st.columns([1,2])
    with col1:
        st.image(j['snippet.thumbnails.default.url'])
    with col2:
        st.write(f'{j['snippet.title']}')
        x,y =st.columns([1,1])
        with x:
            st.write(f'Views: :green[{j['statistics.viewCount']}]')
            if isinstance (j['snippet.defaultAudioLanguage'],str):#give me value if its string
                st.write(f'Audio: :green[{j['snippet.defaultAudioLanguage']}]')
            else:
                st.write("Audio: :red['Not Given']")
        with y:
            st.write(f'Likes: :red[{j['statistics.likeCount']}]')
    st.divider()