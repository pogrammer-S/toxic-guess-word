from src.model.connect import model
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
    
    def checking_word(self, clean_word: str, session_id: str):
        random_word = return_game_state(session_id)["random_word"]
        if clean_word not in model.key_to_index:
            return "Нет слова"
        elif clean_word.split('_')[1] != "NOUN":
            return "Только существительные"
        elif clean_word == random_word:
            self.new_game()
            return f"Победа {self.help_start()}"
        elif clean_word in return_game_state(session_id)["old_messages"]:
            return "Было"
        else:
            self.old_messages.append(clean_word)
            self.tryers+=1
            #return model_manager.return_most_similar_word(return_game_state(session_id)["random_word"], clean_word, config.MODEL_TOPN)
            return f"Неверно {model_manager.return_most_similar_word(random_word, clean_word)}"
        
    def help(self, session_id: str):
        random_word = return_game_state(session_id)["random_word"]
        most_similar_word = model_manager.return_most_similar_on_start(random_word, config.MODEL_TOPN)
        return f"Помощь {most_similar_word}"
    
    def help_start(self):
        most_similar_word = model_manager.return_most_similar_on_start(self.random_word, config.MODEL_TOPN)
        return f"{most_similar_word}"

