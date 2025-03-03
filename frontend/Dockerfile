# Use a lightweight Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

