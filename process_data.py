import pandas as pd
import nltk
import ast # A library to help convert string-to-list
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle

# --- 1. Load Data ---
# (مطمئن شو که اسم فایل‌های CSV دانلودی همینه)
print("Loading data...")
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# --- 2. Merge & Clean Data ---
# ادغام دو دیتافریم بر اساس ستون عنوان
movies = movies.merge(credits, on='title')

# انتخاب ستون‌های کلیدی که برای پیشنهاد لازم داریم
# We only keep columns that influence recommendations
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# حذف سطرهایی که داده خالی دارند (چون بدون اینها نمی‌توان پیشنهاد داد)
movies.dropna(inplace=True)

# --- 3. Pre-processing Helper Functions (The Tricky Part) ---

# ستون‌های 'genres', 'keywords', 'cast', 'crew' به صورت رشته (String) هستند
# ما باید آنها را به لیست پایتون تبدیل کنیم
def convert_json_to_list(obj_str):
    """Converts a string representation of a list of dicts into a list of names."""
    try:
        # ast.literal_eval is safer than eval()
        obj_list = ast.literal_eval(obj_str)
        names = [item['name'] for item in obj_list]
        return names
    except:
        return []

# برای ستون بازیگران، فقط 3 بازیگر اصلی را نگه می‌داریم
def get_top_3_cast(obj_str):
    """Gets the top 3 cast members."""
    try:
        obj_list = ast.literal_eval(obj_str)
        names = [item['name'] for item in obj_list[:3]] # Get first 3
        return names
    except:
        return []

# برای ستون عوامل، فقط کارگردان را استخراج می‌کنیم
def get_director(obj_str):
    """Finds the director from the crew list."""
    try:
        obj_list = ast.literal_eval(obj_str)
        for item in obj_list:
            if item['job'] == 'Director':
                return [item['name']]
        return []
    except:
        return []

print("Cleaning data (JSON and Text)...")
# اعمال تابع‌های کمکی روی ستون‌ها
movies['genres'] = movies['genres'].apply(convert_json_to_list)
movies['keywords'] = movies['keywords'].apply(convert_json_to_list)
movies['cast'] = movies['cast'].apply(get_top_3_cast)
movies['crew'] = movies['crew'].apply(get_director)

# حذف فاصله‌ها در نام‌ها (خیلی مهم)
# This prevents "Sam Worthington" and "Sam Mendes" from being treated as the same "Sam"
def remove_spaces(str_list):
    return [item.replace(" ", "") for item in str_list]

movies['genres'] = movies['genres'].apply(remove_spaces)
movies['keywords'] = movies['keywords'].apply(remove_spaces)
movies['cast'] = movies['cast'].apply(remove_spaces)
movies['crew'] = movies['crew'].apply(remove_spaces)

# --- 4. Create "Tags" ---
# ساختن یک ستون واحد که تمام اطلاعات کلیدی را در خود دارد
# We combine all key features into one giant text "tag"
movies['overview'] = movies['overview'].apply(lambda x: x.split()) # Convert overview to list
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# تبدیل لیست برچسب‌ها به یک رشته واحد
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
# تبدیل به حروف کوچک
movies['tags'] = movies['tags'].apply(lambda x: x.lower())

# --- 5. Stemming (رﯾﺷﻪﯾﺎﺑﯽ) ---
# 'loved', 'loving', 'love' همگی به 'love' تبدیل می‌شوند
ps = PorterStemmer()

def stem(text):
    """Stems a given text."""
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

print("Stemming text data...")
movies['tags'] = movies['tags'].apply(stem)

# --- 6. Vectorization (Core ML) ---
# تبدیل متن به بردار عددی
# We use CountVectorizer (max_features=5000 means keep the 5000 most common words)
cv = CountVectorizer(max_features=5000, stop_words='english')

print("Vectorizing data...")
vectors = cv.fit_transform(movies['tags']).toarray()

# --- 7. Calculate Similarity ---
# محاسبه شباهت کسینوسی بین تمام بردارها
print("Calculating similarity matrix...")
similarity = cosine_similarity(vectors)

# --- 8. Save the Model Files ---
# ما به دو فایل برای اپلیکیشن Streamlit نیاز داریم:
# 1. لیست فیلم‌ها (برای منوی Dropdown)
# 2. ماتریس شباهت (برای پیدا کردن فیلم‌های مشابه)

# فقط دیتافریم اصلی را ذخیره می‌کنیم (نه همه‌چیز)
# We only need the title and movie_id for the app
movies_list_df = movies[['movie_id', 'title']]

pickle.dump(movies_list_df, open('movies_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✅ Processing complete! Model files saved as:")
print("1. movies_list.pkl")
print("2. similarity.pkl")