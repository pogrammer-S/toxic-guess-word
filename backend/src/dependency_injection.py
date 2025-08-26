from src.domain.interfaces import IGameEngine, IGameRepository, IWordModel
from src.infrastructure.word_model import WordModel
from src.infrastructure.game_repository import GameRepository
from src.domain.game_engine import GameEngine
from src.application.game_service import GameService

class DependencyContainer:
    """Контейнер для управления зависимостями"""
    
    def __init__(self):
        self._word_model: IWordModel = None
        self._game_repository: IGameRepository = None
        self._game_engine: IGameEngine = None
        self._game_service: GameService = None
    
    @property
    def word_model(self) -> IWordModel:
        """Возвращает экземпляр модели слов (singleton)"""
        if self._word_model is None:
            self._word_model = WordModel()
        return self._word_model
    
    @property
    def game_repository(self) -> IGameRepository:
        """Возвращает экземпляр репозитория игр (singleton)"""
        if self._game_repository is None:
            self._game_repository = GameRepository()
        return self._game_repository
    
    @property
    def game_engine(self) -> IGameEngine:
        """Возвращает экземпляр игрового движка (singleton)"""
        if self._game_engine is None:
            self._game_engine = GameEngine(
                game_repository=self.game_repository,
                word_model=self.word_model
            )
        return self._game_engine
    
    @property
    def game_service(self) -> GameService:
        """Возвращает экземпляр игрового сервиса (singleton)"""
        if self._game_service is None:
            self._game_service = GameService(
                game_engine=self.game_engine,
                game_repository=self.game_repository
            )
        return self._game_service

# Глобальный экземпляр контейнера
container = DependencyContainer()
