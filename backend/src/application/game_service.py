from typing import Optional, Tuple
from src.domain.interfaces import IGameEngine, IGameRepository, GameState, GameStats
from src.infrastructure.game_repository import DatabaseError

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
    
    def get_statistics(self, session_id: str) -> GameStats:
        """Получает статистику для сессии"""
        try:
            return self.game_repository.get_session_stats(session_id)
        except DatabaseError as e:
            raise GameServiceError(f"Ошибка при получении статистики: {e}")

class GameServiceError(Exception):
    """Исключение для ошибок сервисного слоя"""
    pass
