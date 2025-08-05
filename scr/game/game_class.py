from scr.model.connect import nlp, model
from scr.database.db_service import return_game_state
import random

class Game:
    def __init__(self):
        self.random_word = self.new_random_word()
        self.tryers = 0
        self.old_messages = []

    def new_game(self):
        self.random_word = self.new_random_word()
        self.old_messages = []
        self.tryers = 0

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
        if self.add_pos_tag(random_word_tag[0]).split("_")[1] == random_word_tag[1]:
            return False
        return True
    
    def new_random_word(self):
        rand_word = random.choice(list(model.key_to_index.keys()))

        while self.checking_tag(rand_word.split("_")):
            print(f"{rand_word} не удачно, добавляется {self.add_pos_tag(rand_word.split('_')[0]).split('_')[1]}")
            rand_word = random.choice(list(model.key_to_index.keys()))

        print(rand_word)
        return rand_word
    
    def checking_word(self, clean_word: str, message: str, user_ip):
        if clean_word not in model.key_to_index:
            return f"Слово '{message}' отсутствует в модели."
        elif clean_word == return_game_state(user_ip)["random_word"]:
            tryer=return_game_state(user_ip)["random_word"]
            self.new_game()
            return f"Вы победили за {tryer} попыток"
        elif clean_word in return_game_state(user_ip)["old_messages"]:
            return "Это слово уже было"
        else:
            self.old_messages.append(clean_word)
            self.tryers+=1
            return model.most_similar(positive=[self.random_word], negative=[clean_word], topn=3)