from src.model.connect import nlp, model
from src.database.db_service import return_game_state
from main import model_manager, config

class Game:
    def __init__(self):
        self.random_word = model_manager.new_random_word()
        self.tryers = 0
        self.old_messages = []

    def new_game(self):
        self.random_word = model_manager.new_random_word()
        self.old_messages = []
        self.tryers = 0
    
    def checking_word(self, clean_word: str, message: str, user_ip):
        if clean_word not in model.key_to_index:
            return f"Слово '{message}' отсутствует в модели."
        elif clean_word == return_game_state(user_ip)["random_word"]:
            tryer=return_game_state(user_ip)["tryers"]
            self.new_game()
            return f"Вы победили за {tryer} попыток"
        elif clean_word in return_game_state(user_ip)["old_messages"]:
            return "Это слово уже было"
        else:
            self.old_messages.append(clean_word)
            self.tryers+=1
            return model_manager.return_most_similar_word(return_game_state(user_ip)["random_word"], clean_word, config.MODEL_TOPN)