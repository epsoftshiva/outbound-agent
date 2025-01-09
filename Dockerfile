FROM python:3.12-slim

# Install system dependencies for audio and the Azure SDK
RUN apt-get update && apt-get install -y \
    libasound2 \
    libasound2-dev \
    libssl-dev \
    libffi-dev


