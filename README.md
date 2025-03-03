#Dog Breed Assistant

Overview

This project is an **NLP-powered chatbot** for querying dog breed information. 
It uses **FastAPI (backend)** and **Streamlit (frontend)**, with **Faiss** for retrieval.

## Folder Structure
📂 Dog_Breeds/ 
│── 📂 backend/
│ ├── Dockerfile
│ ├── main.py
│ ├── myfunc.py
│ ├── requirements.txt
│── 📂 frontend/
│ ├── Dockerfile
│ ├── app.py
│ ├── requirements.txt
│── 📂 data/
│ ├── akc-data-latest.csv
│ ├── faiss_index.bin
│── docker-compose.yml
└── README.md


How to Run
### **Clone the Repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/dog_breed_assistant.git
cd dog_breed_assistant
```

### **Run with Docker**
```bash
docker-compose up -d --build
```

### **Checks**
Backend → http://localhost:8000/docs
Frontend → http://localhost:8501

### Notes
1. Please wait until the FastAPI server is up on the backend, before proceeding with requests on Streamlit. The following message will be visible:
```bash
docker-compose logs backend
# backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
2. Please make sure that the folder structure is adhered to.


Features

✔️ NLP-Based Question Answering
✔️ Data Analysis with DuckDB
✔️ Faiss-based Vector Search
✔️ Streamlit Chat Interface
✔️ Dockerized for Easy Deployment




