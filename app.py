import streamlit as st
import pickle
import requests
import pandas as pd


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c6179ded5de8f9b1c3976368cd992a42&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')  # Use get to avoid KeyError
    if poster_path:  # Check if poster_path exists
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None  # Return None if no poster found


def recommend(movie):
    movies1 = pd.DataFrame(movies)
    movie_index = int(movies1.loc[movies1['title'] == movie].index[0])
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies1['movie_id'][i[0]]
        poster = fetch_poster(movie_id)
        if poster:  # Check if poster is valid
            recommended_movie_posters.append(poster)
            recommended_movie_names.append(movies['title'][i[0]])

    return recommended_movie_names, recommended_movie_posters


# Load data safely
try:
    st.header('MOVIES RECOMMENDER SYSTEM')
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity_compressed.pkl', 'rb'))

    movie_list = list(movies['title'].values())
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            if i < len(recommended_movie_names):  # Check bounds
                with col:
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])

except FileNotFoundError as e:
    st.error(f"Error loading files: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
