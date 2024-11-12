FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    libx11-dev \
    libgdk-pixbuf2.0-0 \
    libcanberra-gtk-module \
    && wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

RUN useradd python
RUN chown -R python /usr/src/app
USER python

CMD ["python", "main.py"]