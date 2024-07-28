import streamlit as st
import pandas as pd
import sqlite3
from textblob import TextBlob
from datetime import datetime

# Database helper functions
def get_connection():
    return sqlite3.connect('mood_tracker.db')

def add_user(name, phone_number, age):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (name, phone_number, age) VALUES (?, ?, ?)', (name, phone_number, age))
    conn.commit()
    conn.close()

def add_mood_entry(user_id, date, mood, rating, notes, sentiment):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO mood_entries (user_id, date, mood, rating, notes, sentiment) VALUES (?, ?, ?, ?, ?, ?)',
              (user_id, date, mood, rating, notes, sentiment))
    conn.commit()
    conn.close()

def fetch_mood_data(user_id):
    conn = get_connection()
    query = '''
        SELECT date, mood, rating, notes, sentiment
        FROM mood_entries
        WHERE user_id = ?
        ORDER BY date
    '''
    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()
    return df

# Streamlit app
st.title('Mood Tracker App')

# User Registration
st.subheader('Register User')
with st.form(key='user_form'):
    name = st.text_input('Name')
    phone_number = st.text_input('Phone Number')
    age = st.number_input('Age', min_value=1, max_value=120)
    submit_user_button = st.form_submit_button(label='Register')

    if submit_user_button and name and phone_number:
        add_user(name, phone_number, age)
        st.success('User registered successfully!')

# User ID Input
user_id = st.number_input('Enter User ID', min_value=1)

if user_id:
    # Mood logging form
    st.subheader('Log Mood')
    with st.form(key='mood_form'):
        mood = st.text_input('Mood Category (e.g., Happy, Sad)')
        rating = st.slider('Mood Rating (1 to 10)', 1, 10)
        notes = st.text_area('Additional Notes')
        submit_mood_button = st.form_submit_button(label='Log Mood')

        if submit_mood_button:
            sentiment = TextBlob(notes).sentiment.polarity
            add_mood_entry(user_id, datetime.now().date(), mood, rating, notes, sentiment)
            st.success('Mood logged successfully!')

    # Display mood history
    st.subheader('Mood History')
    mood_data = fetch_mood_data(user_id)
    if not mood_data.empty:
        st.dataframe(mood_data)

    # Data export
    st.subheader('Export Mood Data')
    if st.button('Export to CSV'):
        mood_data.to_csv('mood_data.csv', index=False)
        st.success('Data exported to mood_data.csv')
