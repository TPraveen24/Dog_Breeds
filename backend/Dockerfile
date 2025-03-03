# Use a lightweight Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Install the missing Spacy model
RUN python -m spacy download en_core_web_sm

# Copy the FastAPI app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

