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
    
    def checking_word(self, clean_word: str, message: str, user_ip: int):
        random_word = return_game_state(user_ip)["random_word"]
        if clean_word not in model.key_to_index:
            return f"<b>Слово <i>{message}</i> отсутствует в модели.</b>"
        elif clean_word.split('_')[1] != "NOUN":
            return "<b>Только существительные</b>"
        elif clean_word == random_word:
            tryer=return_game_state(user_ip)["tryers"]
            self.new_game()
            return f"<b>Вы победили за {tryer} попыток. Загаданно новое слово</b><br>{self.help(user_ip)}"
        elif clean_word in return_game_state(user_ip)["old_messages"]:
            return "<b>Это слово уже было</b>"
        else:
            self.old_messages.append(clean_word)
            self.tryers+=1
            #return model_manager.return_most_similar_word(return_game_state(user_ip)["random_word"], clean_word, config.MODEL_TOPN)
            return f"<b>Неправильное слово.</b><br><i>Расстояние до правильного: {model_manager.return_most_similar_word(random_word, clean_word)}</i>"
        
    def help(self, user_ip: int):
        random_word = return_game_state(user_ip)["random_word"]
        most_similar_word = model_manager.return_most_similar_on_start(random_word, config.MODEL_TOPN)
        html_list = "".join([f"<li>{word}</li>" for word in most_similar_word])
        return f"<b>Подсказка:</b><br>{html_list}"

