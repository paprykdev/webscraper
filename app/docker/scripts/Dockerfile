# FROM python:3.9-slim
#
# WORKDIR /usr/src/app
#
# COPY requirements.txt .
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
#
# COPY . .
#
# RUN apt-get update && apt-get install -y wget unzip && \
#     wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     apt install -y ./google-chrome-stable_current_amd64.deb && \
#     rm ./google-chrome-stable_current_amd64.deb && \
#     apt-get clean
#

# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

# Set the working directory to /app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Run the command to install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
