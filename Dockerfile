FROM python:3.12-slim

# Install system dependencies for audio and the Azure SDK
RUN apt-get update && apt-get install -y \
    libasound2 \
    libasound2-dev \
    libssl-dev \
    libffi-dev

# Set the working directory
WORKDIR /app

# Copy the app code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py"]
