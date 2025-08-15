import random
from .connect import model, nlp

class ModelManager:
    def __init__(self):
        pass

    def add_pos_tag(self, word):
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        if word.lower() in days:
            return f"{word}_PROPN"
        
        if word.endswith(('тельный', 'альный', 'яльный')):
            return f"{word}_ADJ"
        
        doc = nlp(word)
        pos = doc[0].pos_

        if pos == 'VERB' and word.endswith(('ный', 'ая', 'ое')):
            pos = 'ADJ'
        
        return f"{word}_{pos}"
    
    def checking_tag(self, random_word_tag : list):
        if self.add_pos_tag(random_word_tag[0]).split("_")[1] == random_word_tag[1] and random_word_tag[1]=="NOUN":
            return False
        return True

    def new_random_word(self):
        rand_word = random.choice(list(model.key_to_index.keys()))

        while self.checking_tag(rand_word.split("_")):
            print(f"{rand_word} не удачно, добавляется {self.add_pos_tag(rand_word.split('_')[0]).split('_')[1]}")
            rand_word = random.choice(list(model.key_to_index.keys()))

        print(rand_word)
        return rand_word
    
    def return_most_similar_word(self, random_word: str, clean_word: str):
        vocab = model.key_to_index
        return abs(vocab.get(random_word) - vocab.get(clean_word))
    
    def return_most_similar_on_start(self, random_word: str, topn: int):
        return model.most_similar(positive=[random_word], topn=topn)