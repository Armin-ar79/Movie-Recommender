# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python, Pandas, Scikit-learn, and Streamlit. This application suggests 5 similar movies based on a user's selection, complete with movie posters fetched in real-time.

**[View the Live Demo Here!](https://movie-recommender-rnbemsm5ez6qkhcmuqjzzj.streamlit.app/)** ---

## 🌟 Features

- **Content-Based Filtering:** Recommends movies based on shared metadata (overview, genres, keywords, cast, and crew).
- **Interactive UI:** Built with **Streamlit** for a clean, fast, and easy-to-use web interface.
- **Dynamic Poster Fetching:** Uses the **TMDB API** to fetch and display movie posters for a rich user experience.
- **Efficient Vectorization:** Employs `CountVectorizer` and **Cosine Similarity** from Scikit-learn to find the closest matches among thousands of movies.
- **Data Preprocessing:** Includes robust functions to parse and clean complex JSON-like string data from the source CSVs.

## 🛠️ Tech Stack

- **Language:** Python
- **Core Libraries:** Pandas, Scikit-learn, NLTK
- **Web Framework:** Streamlit
- **API:** TMDB (The Movie Database) for metadata
- **Deployment:** Streamlit Community Cloud

---

## 🚀 How to Run Locally

To run this project on your local machine, follow these steps:

### 1. Prerequisites

- Python 3.9 - 3.11
- Git and Git LFS (for the large `.pkl` files)

### 2. Get the Data
This project uses the **TMDB 5000 Movie Dataset** from Kaggle. Because the raw files are too large for this repository, please download them from the link below and place them in the root of the project folder:

* **Download Link:** [TMDB 5000 Movie Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
* **Files needed:** `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`

### 3. Clone the Repository
```bash
git clone [https://github.com/Armin-ar79/Movie-Recommender.git](https://github.com/Armin-ar79/Movie-Recommender.git)
cd Movie-Recommender

# Pull the large model files
git lfs pull

### 4. Install Dependencies
Install the required Python packages:
pip install -r requirements.txt

### 5. Get Your API Key
This app requires an API key from TMDB to fetch posters.

  1. Create a free account at themoviedb.org.
  2. Go to your Settings > API section and copy your API Key (v3 auth).

### 6. Run the Preprocessing Script
Before running the app, you must first process the raw CSVs into the similarity model.
py process_data.py

This will generate two files: movies_list.pkl and similarity.pkl.

### 7. Run the Streamlit App
Create a file named .streamlit/secrets.toml and add your API key in this format:
TMDB_API_KEY = "YOUR_API_KEY_HERE"

Now, run the app:
py -m streamlit run app.py

Your app should now be running locally at http://localhost:8501.

Developed by Armin Arbabi
