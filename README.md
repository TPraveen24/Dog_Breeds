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

###Run with Docker
docker-compose up -d --build

#Checks:
Backend → http://localhost:8000/docs
Frontend → http://localhost:8501

Features

✔️ NLP-Based Question Answering
✔️ Data Analysis with DuckDB
✔️ Faiss-based Vector Search
✔️ Streamlit Chat Interface
✔️ Dockerized for Easy Deployment




