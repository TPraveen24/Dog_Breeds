from fastapi import FastAPI, Query
import pandas as pd
import duckdb
from myfunc import extract_query_details, process_analytical_query, get_best_answer
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Loading dataset
df = pd.read_csv("data/dog_breeds.csv",index_col=0)
df.reset_index(inplace=True)  # Move it back to a column
df.rename(columns={"index": "breed"}, inplace=True)  # Rename it properly

#Handling empty numeric columns
numeric_columns = ["popularity", "min_height", "max_height", "min_weight", "max_weight", "min_expectancy", "max_expectancy"]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert valid numbers, set invalid values to NaN
    df[col].fillna(0, inplace=True)  # Replace NaN with 0

# Handling missing values
df.fillna("NA", inplace=True)  

# Convert DataFrame to DuckDB table
con = duckdb.connect(database=":memory:")
con.execute("CREATE TABLE breeds AS SELECT * FROM df")
con.execute("CREATE INDEX idx_popularity ON breeds(popularity)")
con.execute("CREATE INDEX idx_lifespan ON breeds(max_expectancy)")
con.execute("CREATE INDEX idx_height ON breeds(min_height)")
con.execute("CREATE INDEX idx_weight ON breeds(max_weight)")


# Loading Sentence Transformer for Faiss-based retrieval
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# Encode dataset for Faiss search
text_embeddings = embedding_model.encode(df["description"].tolist(), convert_to_tensor=False)
embedding_dim = text_embeddings.shape[1]



@app.post("/ask/")
def ask_question(question: str = Query(..., description="Ask any dog-related question"),user_id: str = Query(...)):
    """Routes the question to either the NLP or Analytical processing pipeline."""

    query_details = extract_query_details(question)

    # If the query contains a metric, always use analytical processing
    if query_details["metric"]:
        return {
            "answer": process_analytical_query(con,question)
        }

    # Otherwise, use NLP processing
    return {
        "answer": get_best_answer(df,embedding_model,question)
    }
