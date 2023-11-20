FROM python:3.11-slim-bullseye
# FROM python:3.10-slim
# FROM ts/python 

# Set environment variables
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

# Update and install necessary packages (needed for postgres conneciton)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Create a working directory
WORKDIR /client_family

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app will run on
EXPOSE 5000

# Start the application
CMD ["flask", "--app", "__init__", "run", "--host", "0.0.0.0"]