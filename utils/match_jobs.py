def recommend_jobs(resume_text, job_df, top_n=5):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    if job_df.empty:
        return pd.DataFrame(columns=["Title", "Description", "match_score"])

    job_df = job_df.copy()

    # Combine title and description for matching
    job_df["combined"] = job_df["Title"].fillna("") + " " + job_df["Description"].fillna("")

    # Combine resume and job texts
    texts = [resume_text] + job_df["combined"].tolist()

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Cosine similarity of resume with each job
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Add match score to DataFrame
    job_df["match_score"] = cosine_sim

    # Sort and return top N
    top_matches = job_df.sort_values(by="match_score", ascending=False).head(top_n)

    return top_matches[["Title", "Description", "match_score"]]
