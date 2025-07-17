from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_jobs(resume_text, jobs_df, top_n=5):
    jobs_df = jobs_df.copy()

    # Combine job title + description
    jobs_df["combined"] = jobs_df["Title"].fillna("") + " " + jobs_df["Description"].fillna("")

    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text] + jobs_df["combined"].tolist())

    resume_vector = vectors[0]
    job_vectors = vectors[1:]

    # Similarity score
    similarities = cosine_similarity(resume_vector, job_vectors).flatten()
    jobs_df["match_score"] = similarities

    # Match keywords
    resume_tokens = set(resume_text.lower().split())
    matched_keywords_list = []

    feature_names = vectorizer.get_feature_names_out()
    resume_tfidf = resume_vector.toarray().flatten()

    for i in range(job_vectors.shape[0]):
        job_vector = job_vectors[i].toarray().flatten()
        matches = [
            feature_names[j] for j in range(len(feature_names))
            if resume_tfidf[j] > 0 and job_vector[j] > 0 and feature_names[j] in resume_tokens
        ]
        matched_keywords_list.append(", ".join(matches[:5]))  # Limit to 5 keywords

    jobs_df["Matched Keywords"] = matched_keywords_list

    # Sort by score and select top N
    top_jobs = jobs_df.sort_values(by="match_score", ascending=False).head(top_n)

    return top_jobs[["Title", "Description", "match_score", "Matched Keywords"]]
