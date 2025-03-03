
import spacy
import faiss
import numpy as np
import torch
import re
from transformers import pipeline

# Loading NLP model for Question Answering (chose distilbert because of CPU processing)
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", device=0 if torch.cuda.is_available() else -1)



# Loading NLP model for extracting query details
nlp = spacy.load("en_core_web_sm")

# Create Faiss index for fast similarity search
#faiss_index = faiss.IndexFlatL2(embedding_dim)
#faiss_index.add(np.array(text_embeddings, dtype=np.float32))


#faiss.write_index(faiss_index, "faiss_index.bin")

#Reading Faiss index from file
faiss_index = faiss.read_index("data/faiss_index.bin")

def extract_query_details(question):
    """Extracts numerical and categorical details dynamically from the question."""
    doc = nlp(question.lower())

    extracted_info = {
        "metric": None,  # e.g., "popularity", "max_expectancy"
        "limit": None,  # Default: 5 results
        "comparison": None,  # e.g., ">", "<"
        "value": None  # e.g., 60 for height
    }

    # Recognize numbers and comparisons
    for token in doc:
        if token.like_num:
            num_value = int(token.text)
            # Check if the number is likely a limit (e.g., "top 7", "top 10")
            if any(keyword in question for keyword in ["top", "most", "least", "smallest", "largest"]):
                extracted_info["limit"] = num_value
                print("NUM ",num_value)
            else:
                extracted_info["value"] = num_value

            extracted_info["value"] = float(token.text)
        elif token.text in ["top", "most", "largest", "highest"]:
            extracted_info["comparison"] = "DESC"
        elif token.text in ["smallest", "lowest", "least"]:
            extracted_info["comparison"] = "ASC"
        elif token.text in ["more", "above", "over", "greater"]:
            extracted_info["comparison"] = ">"
        elif token.text in ["less", "below", "under", "fewer"]:
            extracted_info["comparison"] = "<"

    # Extract the metric (column name)
    column_mapping = {
        "popular": "popularity",
        "lifespan": "max_expectancy",
        "height": "min_height",
        "weight": "max_weight"
    }
    for word in column_mapping.keys():
        if word in question.lower():
            extracted_info["metric"] = column_mapping[word]

    return extracted_info

def get_best_answer(df,embedding_model,question):
    """Handles NLP-based descriptive questions using Faiss + BERT."""
    
    # Convert question to an embedding for Faiss search
    question_embedding = embedding_model.encode([question], convert_to_tensor=False)

    # Find the 5 most relevant breed descriptions
    _, best_match_idx = faiss_index.search(np.array(question_embedding, dtype=np.float32), 5)
    
    # Extract top matches
    relevant_descriptions = " ".join(df.iloc[i]["description"] for i in best_match_idx[0])

    # Use BERT to extract the answer from the top matches
    result = qa_pipeline(question=question, context=relevant_descriptions)
    
    return result["answer"]

def process_analytical_query(con,question):
    """Handles analytical queries using DuckDB."""
    query_details = extract_query_details(question)
    metric = query_details["metric"]
    comparison = query_details["comparison"]
    value = query_details["value"]
    limit = query_details.get("limit", 5)

    if metric:
        if comparison in [">", "<"] and value is not None:
            query = f"""SELECT breed, {metric} FROM breeds WHERE CAST({metric} AS FLOAT) {comparison} {value} ORDER BY CAST({metric} AS FLOAT) DESC"""
        elif comparison in ["DESC", "ASC"]:
            query = f"""SELECT breed, {metric} FROM breeds ORDER BY {metric} {comparison}"""
        else:
            query = f"""SELECT breed, {metric} FROM breeds ORDER BY {metric} DESC"""


        if limit:
            query += f" LIMIT {limit}"


        result_df = con.execute(query).fetchdf()
        return result_df.to_dict(orient="records")

    return "No relevant data found."
