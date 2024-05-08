import pandas as pd
import streamlit as st
import pickle
import pandas as pd
import requests

import time

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8acca5b161b26e0667e899b51a8c16c2&language=en-US".format(movie_id)
    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(url)
            data = response.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            time.sleep(1)  # Wait for a second before retrying
    return None  # Return None if all retries fail


def recommend(movie):
    movie_index = movies[movies["title"] == movie].index

    if len(movie_index) == 0:
        print(f"Movie '{movie}' not found.")
        return

    movie_index = movie_index[0]  # Extract the index from the list
    # it finds the distances of the movie from that it chooses minimum five distances
    # Calculate similarity scores using the similarity matrix (assuming you have it defined)
    distances = similarity[movie_index]

    # Sort and get the indices of most similar movies (excluding the movie itself)
    movie_indices = sorted(range(len(distances)), key=lambda i: distances[i], reverse=True)[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for index in movie_indices:
        recommended_movies.append(movies.iloc[index]["title"])
        recommended_movies_posters.append(fetch_poster(movies.iloc[index].movie_id))

    return recommended_movies,recommended_movies_posters




movies_dict=pickle.load(open("movie_dict1.pkl","rb"))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open("similarity.pkl","rb"))
st.title("movie recommendation system")
option = st.selectbox(
"How would you like to be contacted?",
movies["title"].values)


if st.button("Recommend"):
    recommendations,posters=recommend(option)
    col1, col2, col3, col4,col5 = st.columns(5)

    with col1:
        st.header(recommendations[0])
        st.image(posters[0])
    with col2:
        st.header(recommendations[1])
        st.image(posters[1])
    with col3:
        st.header(recommendations[2])
        st.image(posters[2])
    with col4:
        st.header(recommendations[3])
        st.image(posters[3])
    with col5:
        st.header(recommendations[4])
        st.image(posters[4])





