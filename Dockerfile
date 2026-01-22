# 1. Use a lightweight Linux-based Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install System Dependencies
# 'build-essential' gives us the C++ compilers you were missing on Windows.
# 'git' is needed to download the Senko library.
# 'ffmpeg' is needed for audio processing.
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy the requirements file
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Install the library that was failing on Windows
# Since we have 'build-essential' now, this will succeed!
RUN pip install git+https://github.com/narcotic-sh/senko

# 7. Copy the rest of your project files
COPY . .

# 8. Expose the port Streamlit runs on
EXPOSE 8501

# 9. Run the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]