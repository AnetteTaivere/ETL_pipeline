FROM python:3.10

WORKDIR app
COPY app/* /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# For Postgresql 
EXPOSE 5432

# Env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "crawler.py"]
