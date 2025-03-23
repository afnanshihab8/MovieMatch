import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Movie

nltk.download('stopwords')
nlp = spacy.load("en_core_web_md")  # Load spaCy's medium-sized language model

def process_text(text):
    """Preprocess text by removing stopwords and lemmatizing."""
    doc = nlp(text.lower())
    return " ".join([token.lemma_ for token in doc if not token.is_stop])

# def recommend_movies_based_on_words(user_words):
#     movies = Movie.objects.all()
#     if not movies:
#         return []  # Return empty if no movies exist

#     user_input = " ".join(user_words)
    
#     movie_texts = []
#     for movie in movies:
#         genres = ", ".join([g.name for g in movie.genres.all()]) if hasattr(movie, 'genres') else ""
#         tags = movie.tags if movie.tags else ""
#         description = movie.description if movie.description else ""
#         full_text = f"{genres} {tags} {description}"
#         movie_texts.append(process_text(full_text))

#     # Convert user input into processed text
#     user_input_processed = process_text(user_input)
    
#     # TF-IDF Vectorization
#     vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = vectorizer.fit_transform(movie_texts + [user_input_processed])

#     # Compute cosine similarity between user input and all movies
#     similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

#     # Get top movie recommendations
#     top_indices = np.argsort(similarity_scores)[::-1][:5]  # Top 5 matches

#     recommended_movies = [movies[i] for i in top_indices if similarity_scores[i] > 0]

#     return recommended_movies

def recommend_movies_based_on_words(user_words):
    movies = Movie.objects.all()
    if not movies:
        print("No movies found in the database.")  # Debugging
        return []  

    user_input = " ".join(user_words)
    print("User Input:", user_input)  # Debugging
    
    movie_texts = []
    for movie in movies:
        genres = ", ".join([g.name for g in movie.genres.all()]) if hasattr(movie, 'genres') else ""
        tags = movie.tags if movie.tags else ""
        description = movie.description if movie.description else ""
        full_text = f"{genres} {tags} {description}"
        processed_text = process_text(full_text)
        movie_texts.append(processed_text)

    print("Processed Movie Texts:", movie_texts)  # Debugging

    # Convert user input into processed text
    user_input_processed = process_text(user_input)
    print("Processed User Input:", user_input_processed)  # Debugging
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(movie_texts + [user_input_processed])

    # Compute cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    print("Similarity Scores:", similarity_scores)  # Debugging

    # Get top movie recommendations
    top_indices = np.argsort(similarity_scores)[::-1][:5]
    recommended_movies = [movies[i] for i in top_indices if similarity_scores[i] > 0]

    print("Recommended Movies:", recommended_movies)  # Debugging
    return recommended_movies
