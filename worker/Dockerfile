FROM python:3.12.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Run the application
CMD ["python", "-m", "main"]