FROM python:3.12-slim-bookworm

# Set environment variables for better Python behavior in Docker
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing .pyc files
ENV PYTHONUNBUFFERED 1     # Prevents Python from buffering stdout and stderr

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
# and install the Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the working directory
COPY . .

# Expose the port your application will listen on
EXPOSE 8000 

# RUN THE API
CMD ["python", "server.py"]
