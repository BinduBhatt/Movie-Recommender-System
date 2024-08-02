import streamlit as st
import pickle
import pandas as pd
from operator import itemgetter
import requests
custom_css = """
<style>
.st-emotion-cache-1r4qj8v {
    background-color: #e68189;
    ;
}

h1, h2, h3, h4, h5, h6 {
    color: #201269;
}

.text, .stText {
    color: #555555;
    font-size: 16px;
}

.stButton > button {
    background-color: #4CAF50;
    color: white;
}

.stButton > button:hover {
    background-color: #45a049;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

def poster(movie_id):
    url = requests.get('https://api.themoviedb.org/3/movie/ {}?api_key=d25823fb281ad0034c0349eb6229f643'.format(movie_id))
    data = url.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def fetch_info(movie_id):
    url = requests.get('https://api.themoviedb.org/3/movie/ {}?api_key=d25823fb281ad0034c0349eb6229f643'.format(movie_id))
    data = url.json()
    return data['homepage']

def fetch_reviews(movie_id):

    url = requests.get("https://api.themoviedb.org/3/movie/{}/reviews?api_key=d25823fb281ad0034c0349eb6229f643".format(movie_id))
    data = url.json()
    reviews = []
    results= data.get('results', [])
    for i in results:
        author = i['author_details'].get('name', 'Anonymous')
        rating = i['author_details'].get('rating', 'No rating')
        review = i.get('content', 'No Review')
        reviews.append({'author': author, 'rating': rating, 'review': review})
    return reviews

def recommendation(movie):
    index = movies[movies['title']== movie].index[0]
    distance = similarity[index]
    movie_list = sorted(enumerate(distance), reverse=True, key=itemgetter(1))[1:6]
    recommended_movies = []
    posters=[]
    homepages=[]
    reviews = []

    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]]['title'])
        posters.append(poster(movies.iloc[i[0]]['movie_id']))
        homepages.append(fetch_info(movies.iloc[i[0]]['movie_id']))
        reviews.append(fetch_reviews(movies.iloc[i[0]]['movie_id']))

    return recommended_movies, posters, homepages, reviews

movies = pickle.load(open('Movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies)
mov_list = movies['title'].values
st.title('Movie Recommendation System :sunglasses:')
# st.snow()

option = st.selectbox(
    "**Which Movie have you seen?**", mov_list)

st.write("**You selected:**", option)

if st.button("Recommend", type='primary', key = "recommend_button"):
    recommended_movies, posters, homepages, reviews = recommendation(option)
    cols = st.columns(len(recommended_movies))

    for i, col in zip(range(len(recommended_movies)),cols):
        with col:
            st.text(recommended_movies[i])
            st.image(posters[i])

            if homepages[i]:
                st.link_button("More Info", homepages[i])
            else:
                st.write("No Info Available")


            review_key = f"review_button{i}"
            if reviews[i]:
                # st.button("Reviews", type='primary', key=review_key)
                total_rating = 0
                rating_count = 0


                for review in reviews[i]:
                    if review['rating'] is not None:
                        total_rating += review['rating']
                        rating_count += 1
                avg_rating = round((total_rating / rating_count),1) if rating_count>0 else "No Rating"
                st.write(f"**Rating**: {avg_rating}")
            else:
                st.write("**No Reviews**")

