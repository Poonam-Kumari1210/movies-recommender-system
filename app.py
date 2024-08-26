import streamlit as st
import pickle
import requests
import pandas as pd


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c6179ded5de8f9b1c3976368cd992a42&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    print(data)
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movies1 = pd.DataFrame(movies)
    movie_index = int(movies1.loc[movies1['title'] == movie].index[0])
    # movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    # movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        #movie_id = movies.iloc[i[0]].movie_id

        movie_id = movies1['movie_id'][i[0]]
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies['title'][i[0]])

    return recommended_movie_names, recommended_movie_posters


st.header('MOVIES RECOMMENDER SYSTEM')
movies = pickle.load(open('movie_list.pkl', 'rb'))

print(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))

#movie_list = list(movies['title'].values)
movie_list = list(movies['title'].values())

#movie_list = list(movies['title'].dropna().values)
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

# movies_dict = pickle.load(open('movie_list.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl','rb'))
# st.title('MOVIES RECOMMENDER SYSTEM')
# selected_movie_name = st.selectbox("How would you like to be contacted?",movies['title'].values)
#
# if st.button("Recommend"):
#     recommendations = recommend(selected_movie_name)
#     for i in recommendations:
#         st.write(i)
