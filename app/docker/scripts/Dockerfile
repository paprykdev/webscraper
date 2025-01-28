# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

# Set the working directory to /app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Run the command to install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
