import streamlit as st
import pandas as pd
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Spotify API authentication
sp = Spotify(auth_manager=SpotifyOAuth(client_id = '2bc67b94571f4eeaa7280e6f4b2e108c', # Replace with your Client ID
                                       client_secret = '081a49d8e041495ca80cf5b7d89e541a',
                                       redirect_uri='http://localhost:8501/',
                                       scope='playlist-read-private'))

# Define moods and associated playlist IDs (you can adjust based on your playlists)
mood_playlists = {
    'happy': '5m7Pu3FDIdgfAuyRTcRJmH',  # Corrected: Removed the query parameter
    'sad': '2sOMIgioNPngXojcOuR4tn',   # Corrected: Removed the query parameter
    'romantic': '0vcYf0AWNNvesTKl6OlQW9',  # Corrected: Removed the query parameter
    'energetic': '3JOShGvo7r1lLQ7Xa7drwg'   # Corrected: Removed the query parameter
}


# Streamlit app title
st.title("Mood-Based Music Explorer")
st.markdown("### Find songs based on your mood! 🎶")
st.markdown("Select your mood from the dropdown menu below to explore the perfect playlist.")

# Mood selection dropdown
mood_options = list(mood_playlists.keys())
selected_mood = st.selectbox("Select your mood:", mood_options)

# Fetch songs based on selected mood
if selected_mood:
    playlist_id = mood_playlists[selected_mood]

    try:
        results = sp.playlist_tracks(playlist_id)

        # Prepare data for display
        songs_data = []
        for item in results['items']:
            track = item['track']
            songs_data.append({
                'artist': track['artists'][0]['name'],
                'song': track['name'],
                'spotify_link': track['external_urls']['spotify']
            })
        
        # Convert to DataFrame
        songs_df = pd.DataFrame(songs_data)

        # Display results
        if not songs_df.empty:
            st.write(f"### Songs for mood: {selected_mood}")
            for index, row in songs_df.iterrows():
                st.markdown(f"**{row['song']}** by {row['artist']}")
                st.markdown(f"[Listen on Spotify]({row['spotify_link']})")
                st.markdown("---")  # Separator for each song
        else:
            st.write("No songs found for this mood.")
    except Exception as e:
        st.write("An error occurred while fetching songs.")
        st.write(e)
