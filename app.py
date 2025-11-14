import streamlit as st
import pickle
import pandas as pd
import requests # برای گرفتن پوستر فیلم از API

# --- تابع دریافت پوستر ---
# ما از API سایت TMDB برای گرفتن پوستر استفاده می‌کنیم
def fetch_poster(movie_id):
    try:
        api_key = "TMDB_API_KEY" # <-- !!اینجا کلید API خود را بگذارید!!
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url)
        response.raise_for_status() # بررسی خطاهای HTTP
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            # ساخت URL کامل پوستر
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
    return None # اگر پوستر نبود یا خطا داد

# --- تابع اصلی پیشنهاددهنده ---
def recommend(movie_title):
    # پیدا کردن ایندکس فیلمی که انتخاب شده
    try:
        movie_index = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        st.error("Movie not found in the database.")
        return [], []

    # گرفتن لیست شباهت‌های آن فیلم با بقیه
    distances = similarity[movie_index]
    
    # مرتب‌سازی فیلم‌ها بر اساس شباهت (از بیشترین به کمترین)
    # [1:6] یعنی 5 فیلم مشابه (چون اولی خودش است)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        
        # گرفتن پوستر
        poster = fetch_poster(movie_id)
        
        recommended_movies.append(movie_title)
        recommended_posters.append(poster)
        
    return recommended_movies, recommended_posters

# --- بارگذاری فایل‌های مدل ---
# (این فایل‌ها باید کنار app.py باشند)
try:
    movies_dict = pickle.load(open('movies_list.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict) # تبدیل دیکشنری به دیتافریم
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files (movies_list.pkl or similarity.pkl) not found. Please run process_data.py first.")
    st.stop() # توقف اجرای اپلیکیشن

# --- ساخت رابط کاربری Streamlit ---

st.set_page_config(layout="wide") # استفاده از تمام عرض صفحه
st.title('🎬 Movie Recommendation System')

# منوی کشویی برای انتخاب فیلم
selected_movie_name = st.selectbox(
    'Select a movie you like, and we will recommend similar ones:',
    movies['title'].values
)

# دکمه "Recommend"
if st.button('Recommend'):
    st.subheader("Here are your recommendations:")
    names, posters = recommend(selected_movie_name)
    
    # نمایش پوسترها در 5 ستون
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i in range(len(names)):
        with columns[i]:
            st.text(names[i])
            if posters[i]:
                st.image(posters[i])
            else:
                st.write("(No poster available)")