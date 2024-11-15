FROM python:3.8
WORKDIR /app
COPY . .
RUN apt-get update && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8050
CMD ["python", "app.py", "--host=0.0.0.0", "--port=8050"]