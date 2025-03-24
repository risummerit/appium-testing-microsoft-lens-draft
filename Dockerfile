FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Include Android tools and ADB if needed
RUN apt-get update && \
    apt-get install -y adb curl unzip openjdk-17-jdk libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Copy wait script *before* declaring ENTRYPOINT
COPY wait-for-appium.sh /wait-for-appium.sh
RUN chmod +x /wait-for-appium.sh

# Run wait script that calls pytest
ENTRYPOINT ["/wait-for-appium.sh"]
