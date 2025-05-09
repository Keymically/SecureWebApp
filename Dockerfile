# 1. Use a lightweight Python image
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system packages required for mysql-connector-python
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
# 4. Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the app code
COPY . .

# 6. Copy wait-for-mysql script and make it executable
COPY wait-for-mysql.sh .
RUN chmod +x wait-for-mysql.sh

# 7. Expose port
EXPOSE 5000

# 8. Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 9. Run Flask only after MySQL is reachable
CMD ["./wait-for-mysql.sh"]
