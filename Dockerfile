FROM python:3.13

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Expose port 5000 for Flask
EXPOSE 5000

CMD ["python", "app.py"]

