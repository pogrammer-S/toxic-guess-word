from gensim.models.keyedvectors import KeyedVectors #pip install gensim
import spacy # type: ignore
"""pip install spacy; python -m spacy download ru_core_news_sm"""

try:
    nlp = spacy.load("ru_core_news_sm")
    model = KeyedVectors.load_word2vec_format('./src/model/model.bin', binary=True)
except Exception as e:
    print(f"Ошибка при загрузке модели: {e}")