import json
import logging
from typing import Optional, Tuple, List
from src.domain.interfaces import IGameEngine, IGameRepository, GameState, SimilarWord

class WordParser:
    """Утилитарный класс для парсинга слов"""
    
    @staticmethod
    def parse_previous_words(words_data) -> List[SimilarWord]:
        """Парсит previous_words из БД в список SimilarWord"""
        previous_words = []
        if words_data:
            try:
                # Парсим JSON
                if isinstance(words_data, str):
                    parsed_data = json.loads(words_data)
                else:
                    parsed_data = words_data
                
                for word_data in parsed_data:
                    if isinstance(word_data, dict):
                        previous_words.append(SimilarWord(
                            word=word_data["word"], 
                            distance=word_data["distance"]
                        ))
            except (json.JSONDecodeError, TypeError) as e:
                logging.error(f"Ошибка парсинга previous_words: {e}")
                # Возвращаем пустой список если не можем распарсить
                previous_words = []
        
        return previous_words

class GameService:
    """Сервисный слой для координации игровой логики"""
    
    def __init__(self, game_engine: IGameEngine, game_repository: IGameRepository):
        self.game_engine = game_engine
        self.game_repository = game_repository
    
    def start_new_game(self, client_ip: Optional[str] = None) -> Tuple[GameState, str]:
        """Начинает новую игру и возвращает состояние игры и session_id"""
        try:
            # Создаем сессию
            session_id = self.game_repository.create_session(client_ip)
            
            # Начинаем игру
            game_state = self.game_engine.start_new_game(session_id)
            
            return game_state, session_id
        except DatabaseError as e:
            raise GameServiceError(f"Ошибка при создании игры: {e}")
    
    def make_guess(self, session_id: str, word: str) -> GameState:
        """Делает попытку угадать слово"""
        try:
            return self.game_engine.make_guess(session_id, word)
        except ValueError as e:
            raise GameServiceError(str(e))
        except DatabaseError as e:
            raise GameServiceError(f"Ошибка при обработке попытки: {e}")
    
    def get_hint(self, session_id: str) -> str:
        """Получает подсказку для текущего слова"""
        try:
            return self.game_engine.get_hint(session_id)
        except ValueError as e:
            raise GameServiceError(str(e))
        except DatabaseError as e:
            raise GameServiceError(f"Ошибка при получении подсказки: {e}")
    
    def get_game_state(self, session_id: str) -> Optional[GameState]:
        """Получает текущее состояние игры"""
        try:
            return self.game_repository.get_game_state(session_id)
        except DatabaseError as e:
            raise GameServiceError(f"Ошибка при получении состояния игры: {e}")
    


class DatabaseError(Exception):
    """Исключение для ошибок базы данных"""
    pass

class GameServiceError(Exception):
    """Исключение для ошибок сервисного слоя"""
    pass
