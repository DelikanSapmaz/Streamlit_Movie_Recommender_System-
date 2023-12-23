import pandas as pd
import streamlit as st
import pickle
import requests

st.set_page_config(layout="wide")

# CSV dosyalarını oku
movies = pd.read_csv('Desktop/new1/tmdb_5000_movies.csv')
credits = pd.read_csv('Desktop/new1/tmdb_5000_credits.csv')

# Streamlit uygulaması
@st.cache_data
def get_data():
    # DataFrame'leri birleştir
    df = pd.merge(movies, credits)
    return df

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=020b311fe0559698373a16008dc6a672&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for x in movies_list:
        movie_id = movies.iloc[x[0]].movie_id
        recommended_movies.append(movies.iloc[x[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('Desktop/new1/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('Desktop/new1/similarity.pkl', 'rb'))

st.title("🍿 ReCommendSTAR 🥤📽")
tabs = st.tabs(["Ana Sayfa", "Model"])

with tabs[0]:
    column_tanıtım, column_veri = st.columns(2)
    column_tanıtım.subheader(' :red[🎥🎬Film Tavsiye Sistemi  ]')
    column_tanıtım.markdown(" Merhaba Film Tavsiye Sistemine Hoşgeldin. Bugün ne izlemek istersin?")
    column_tanıtım.image("Desktop/new1/media/movie.jpg")

    column_veri.subheader(" :red[Veri Seti Hakkında] 👩‍💻")
    column_veri.markdown("Yoğun bir haftasonunun ardından senin zevklerini en iyi bilen ReCommendSTAR beğeneceğin filmleri direk sana sunar. "
                         "TMDB 5000 film veri seti kullanılarak 100 bin film üzerinden bilgiler alınmıştır. "
                         "Budget, Genres, Homepage, id, Keywords, Original_language, Original_title, Overview, Popularity, Production_companies, Production_countries, Release_date, Revenue, Runtime, Spoken_languages, Status, Tagline, Title, Vote_average, Vote_count, Movie_id, Cast, Crew bilgileri ile "
                         "Kullanıcıya en iyi filmi tavsiye etmek için karşınızdayız ")
    df = get_data()
    column_veri.dataframe(df, width=1500)

with tabs[1]:
    st.title('Movie Recommender System')
    selected_movie_name = st.selectbox(
        'How would you like to be contacted?',
        movies['title'].values
    )

    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
