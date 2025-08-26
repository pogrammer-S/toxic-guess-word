from src.domain.interfaces import IGameEngine, IGameRepository, IWordModel, GameState, SimilarWord
from src.config.config import load_config

class GameEngine(IGameEngine):
    """Доменная логика игры - чистая бизнес-логика без зависимостей от инфраструктуры"""
    
    def __init__(self, game_repository: IGameRepository, word_model: IWordModel):
        self.game_repository = game_repository
        self.word_model = word_model
        self.config = load_config()
    
    def start_new_game(self, session_id: str) -> GameState:
        """Начинает новую игру"""
        # Получаем случайное слово
        target_word = self.word_model.get_random_word()
        
        # Создаем начальное состояние игры с пустым списком предыдущих слов
        game_state = GameState(
            target_word=target_word,
            attempts_left=0,  # В начале игры 0 попыток
            previous_words=[],  # Пустой список - слова будут добавляться по мере угадывания
            message="Игра началась! Попробуйте угадать слово.",
            is_completed=False,
            session_id=session_id
        )
        
        # Сохраняем состояние
        self.game_repository.save_game_state(game_state)
        
        return game_state
    
    def make_guess(self, session_id: str, word: str) -> GameState:
        """Делает попытку угадать слово"""
        # Получаем текущее состояние игры
        current_state = self.game_repository.get_game_state(session_id)
        if not current_state:
            raise ValueError("Игра не найдена")
        
        if current_state.is_completed:
            raise ValueError("Игра уже завершена")
        
        # Очищаем и проверяем слово
        clean_word = self.word_model.add_pos_tag(word)
        
        # Валидация слова
        if not self.word_model.is_word_valid(clean_word):
            return self._create_error_state(current_state, "Такого слова нет в словаре")
        
        if clean_word.split('_')[1] != "NOUN":
            return self._create_error_state(current_state, "Можно использовать только существительные")
        
        # Проверяем, не использовалось ли слово ранее
        if self._is_word_used(current_state, clean_word):
            return self._create_error_state(current_state, "Это слово уже использовалось")
        
        # Проверяем, угадано ли слово
        if clean_word == current_state.target_word:
            return self._create_win_state(current_state, clean_word)
        
        # Слово не угадано - получаем подсказку
        return self._create_incorrect_guess_state(current_state, clean_word)
    
    def get_hint(self, session_id: str) -> str:
        """Получает подсказку для текущего слова"""
        current_state = self.game_repository.get_game_state(session_id)
        if not current_state:
            raise ValueError("Игра не найдена")
        
        if current_state.is_completed:
            raise ValueError("Игра завершена")
        
        # Находим самое близкое слово из угаданных пользователем
        if not current_state.previous_words:
            return "Сначала сделайте хотя бы одну попытку угадать слово"
        
        closest_guess = min(current_state.previous_words, key=lambda x: x.distance)
        
        # Получаем слово, которое находится между загаданным и самым близким угаданным
        # Сначала добавляем тег к слову пользователя
        closest_guess_with_tag = self.word_model.add_pos_tag(closest_guess.word)
        hint_word = self.word_model.get_word_between(
            current_state.target_word, 
            closest_guess_with_tag
        )
        
        # Вычисляем дистанцию для подсказки
        hint_distance = self.word_model.get_most_similar_word(current_state.target_word, hint_word)
        
        # Добавляем подсказку в список предыдущих слов
        new_previous_words = current_state.previous_words + [
            SimilarWord(word=hint_word.split('_')[0], distance=int(hint_distance))
        ]
        
        # Обновляем состояние с подсказкой
        updated_state = GameState(
            target_word=current_state.target_word,
            attempts_left=current_state.attempts_left,
            previous_words=new_previous_words,
            message=f"Подсказка: попробуйте слово '{hint_word.split('_')[0]}'",
            is_completed=current_state.is_completed,
            session_id=session_id
        )
        
        self.game_repository.save_game_state(updated_state)
        
        return updated_state.message
    
    def _create_error_state(self, current_state: GameState, error_message: str) -> GameState:
        """Создает состояние с ошибкой"""
        error_state = GameState(
            target_word=current_state.target_word,
            attempts_left=current_state.attempts_left,
            previous_words=current_state.previous_words,
            message=error_message,
            is_completed=current_state.is_completed,
            session_id=current_state.session_id
        )
        
        self.game_repository.save_game_state(error_state)
        return error_state
    
    def _create_win_state(self, current_state: GameState, correct_word: str) -> GameState:
        """Создает состояние победы"""
        # Добавляем отгаданное слово в список предыдущих слов
        new_previous_words = current_state.previous_words + [
            SimilarWord(word=correct_word.split('_')[0], distance=0)
        ]
        
        win_state = GameState(
            target_word=current_state.target_word,
            attempts_left=current_state.attempts_left + 1,
            previous_words=new_previous_words,
            message="Поздравляем! Вы угадали слово!",
            is_completed=True,
            session_id=current_state.session_id
        )
        
        self.game_repository.save_game_state(win_state)
        return win_state
    
    def _create_incorrect_guess_state(self, current_state: GameState, guess_word: str) -> GameState:
        """Создает состояние при неправильной попытке"""
        # Получаем расстояние до угадываемого слова
        distance = self.word_model.get_most_similar_word(current_state.target_word, guess_word)
        
        # Добавляем угаданное слово в список предыдущих слов
        new_previous_words = current_state.previous_words + [
            SimilarWord(word=guess_word.split('_')[0], distance=int(distance))
        ]
        
        incorrect_state = GameState(
            target_word=current_state.target_word,
            attempts_left=current_state.attempts_left + 1,
            previous_words=new_previous_words,
            message=f"Неверно. Расстояние до слова: {int(distance)}",
            is_completed=False,
            session_id=current_state.session_id
        )
        
        self.game_repository.save_game_state(incorrect_state)
        return incorrect_state
    
    def _is_word_used(self, game_state: GameState, word: str) -> bool:
        """Проверяет, использовалось ли слово ранее"""
        # Проверяем в предыдущих словах (только базовое слово без тега)
        base_word = word.split('_')[0]
        return any(sw.word == base_word for sw in game_state.previous_words)
    

