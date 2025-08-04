FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn 
RUN pip install jinja2 python-multipart
RUN pip install gensim
RUN pip install numpy==1.23.5
RUN pip install spacy==3.5.0
RUN python -m spacy download ru_core_news_sm
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]