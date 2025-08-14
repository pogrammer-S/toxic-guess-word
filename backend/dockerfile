FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download ru_core_news_sm
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]