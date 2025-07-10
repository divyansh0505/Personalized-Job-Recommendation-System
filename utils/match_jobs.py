import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans  # For diversity
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('stopwords')
nltk.download('wordnet')
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())  # Remove special chars
    words = text.split()
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]
    return ' '.join(words)
def recommend_jobs(resume_text, job_df, top_n=5):
    # Input validation
    if job_df.empty:
        return pd.DataFrame(columns=["Title", "Description", "match_score", "matching_keywords"])
    
    # Clean and weight text
    job_df = job_df.copy()
    job_df["combined"] = job_df["Title"].apply(clean_text) + " " + job_df["Description"].apply(clean_text)
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    texts = [clean_text(resume_text)] + job_df["combined"].tolist()
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    job_df["match_score"] = cosine_sim
    
    # Diversity: Cluster and pick best per group
    kmeans = KMeans(n_clusters=min(top_n, len(job_df)))
    job_vectors = vectorizer.transform(job_df["combined"])
    job_df["cluster"] = kmeans.fit_predict(job_vectors)
    recommendations = job_df.loc[job_df.groupby("cluster")["match_score"].idxmax()]
    
    # Explainability and formatting
    resume_vec = tfidf_matrix[0:1]
    recommendations["matching_keywords"] = recommendations["combined"].apply(
        lambda x: get_top_keywords(resume_vec, vectorizer.transform([x]), vectorizer)
    )
    recommendations["match_score"] = (recommendations["match_score"] * 100).round(1)
    
    return recommendations.head(top_n)[["Title", "Description", "match_score", "matching_keywords"]]