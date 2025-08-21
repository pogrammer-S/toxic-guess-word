from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class SimilarWord:
    word: str
    distance: int

@dataclass
class GameState:
    target_word: str
    attempts_left: int
    previous_words: List[SimilarWord]
    last_message: Optional[str] = None
    is_completed: bool = False
    session_id: str = ""

@dataclass
class GameStats:
    total_games: int
    won_games: int
    average_attempts: float



class IGameRepository(ABC):
    """Интерфейс для работы с состоянием игры"""
    
    @abstractmethod
    def get_game_state(self, session_id: str) -> Optional[GameState]:
        pass
    
    @abstractmethod
    def save_game_state(self, game_state: GameState) -> None:
        pass
    
    @abstractmethod
    def create_session(self, client_ip: Optional[str] = None) -> str:
        pass
    
    @abstractmethod
    def get_session_stats(self, session_id: str) -> GameStats:
        pass

class IWordModel(ABC):
    """Интерфейс для работы с моделью слов"""
    
    @abstractmethod
    def add_pos_tag(self, word: str) -> str:
        pass
    
    @abstractmethod
    def get_random_word(self) -> str:
        pass
    
    @abstractmethod
    def get_most_similar_word(self, target_word: str, guess_word: str) -> int:
        pass
    
    @abstractmethod
    def get_most_similar_words(self, target_word: str, topn: int) -> List[SimilarWord]:
        pass
    
    @abstractmethod
    def is_word_valid(self, word: str) -> bool:
        pass
    
    @abstractmethod
    def get_word_between(self, target_word: str, guess_word: str) -> str:
        """Возвращает слово, которое находится между двумя словами в словаре"""
        pass

class IGameEngine(ABC):
    """Интерфейс для игровой логики"""
    
    @abstractmethod
    def start_new_game(self, session_id: str) -> GameState:
        pass
    
    @abstractmethod
    def make_guess(self, session_id: str, word: str) -> GameState:
        pass
    
    @abstractmethod
    def get_hint(self, session_id: str) -> str:
        pass
