from gensim.models.keyedvectors import KeyedVectors #pip install gensim
import spacy # type: ignore
"""pip install spacy; python -m spacy download ru_core_news_sm"""

nlp = spacy.load("ru_core_news_sm")
model = KeyedVectors.load_word2vec_format('scr/model/model.bin', binary=True)