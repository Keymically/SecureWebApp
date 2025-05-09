# 1. Use a lightweight Python image
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements (if you have one) and install dependencies
#    Otherwise install directly
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy your app code
COPY . .

# 5. Expose port 5000
EXPOSE 5000

# 6. Tell Flask how to launch
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 7. Run the app
CMD ["flask", "run"]
