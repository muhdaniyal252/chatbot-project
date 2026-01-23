FROM python:3.11

# Install system deps
RUN apt-get update && apt-get install -y ffmpeg netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Copy wait + entrypoint
COPY wait-for-it.sh /wait-for-it.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /wait-for-it.sh /entrypoint.sh

EXPOSE 8000 8001

ENTRYPOINT ["/entrypoint.sh"]
# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Use it as CMD
CMD ["/start.sh"]