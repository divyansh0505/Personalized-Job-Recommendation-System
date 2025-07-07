from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity   # for matching resume and jobs

def recommend_jobs(resume_text, job_df, top_n=5):
    job_descriptions = job_df["Description"].tolist()
    corpus = job_descriptions + [resume_text]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)

    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])  # matches similarity between resume and each job

    scores = cosine_sim[0]

    top_indices = scores.argsort()[-top_n:][::-1]   # sorts the scores in descending order and gives top n indices
    top_jobs = job_df.iloc[top_indices]

    return top_jobs

