import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os


# Google Drive file ID from share link
file_id = '1gfZEou9sz4i8kQTMpIa5eso3SwZvmj2q'  # Replace with your file's ID

# Output filename
output = 'similarity.pkl'

# Only download if file not already present (caching)
if not os.path.exists(output):
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# Load the pickle file
with open(output, 'rb') as f:
    similarity = pickle.load(f)



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True,key=lambda x:x[1])[1:11]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        #fetch poster
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies,recommend_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

#similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Which movie would you like',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    
    col = st.columns(5)
    for i in range(5):
        with col[i]:
            st.text(names[i])
            st.image(posters[i])

    col2 = st.columns(5)
    for i in range(5, 10):
        with col2[i - 5]:  # shift index to 0–4
            st.text(names[i])
            st.image(posters[i])