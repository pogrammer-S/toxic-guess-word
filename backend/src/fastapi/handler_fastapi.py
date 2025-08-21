from fastapi import APIRouter, Header, HTTPException, Response, status, Request, Depends
from typing import Optional, List
from pydantic import BaseModel, Field, validator
import logging

from src.dependency_injection import container
from src.application.game_service import GameService, GameServiceError
from src.domain.interfaces import SimilarWord, GameState

router = APIRouter(prefix="/api/v1")

# Pydantic модели для API
class SimilarWordResponse(BaseModel):
    word: str
    distance: int

class GameResponse(BaseModel):
    attempts_left: int = Field(ge=0)
    previous_words: List[SimilarWordResponse] = Field(default_factory=list)
    message: Optional[str] = None
    is_completed: bool
    session_id: Optional[str] = None  # Только для /start



class GuessRequest(BaseModel):
    word: str = Field(..., min_length=1)

    @validator('word')
    def word_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Слово не может быть пустым')
        if len(v) > 100:  # разумное ограничение
            raise ValueError('Слово слишком длинное')
        return v.lower().strip()

def get_game_service():
    """Dependency для получения игрового сервиса"""
    return container.game_service

# Middleware для проверки сессии
async def validate_session(
    session_id: str = Header(..., alias="X-Session-Id"),
    game_service: GameService = Depends(get_game_service)
) -> str:
    """Валидирует session_id и проверяет существование игры"""
    try:
        if not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Требуется заголовок X-Session-Id"
            )
        
        # Проверяем существование игры
        game_state = game_service.get_game_state(session_id)
        if not game_state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Игра не найдена. Начните новую игру."
            )
        
        return session_id
    except GameServiceError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при проверке сессии: {str(e)}")

def _convert_game_state_to_response(game_state: GameState, session_id: Optional[str] = None) -> GameResponse:
    """Конвертирует GameState в GameResponse"""
    # Сортируем previous_words по distance в возрастающем порядке
    sorted_words = sorted(game_state.previous_words, key=lambda x: x.distance)
    
    return GameResponse(
        attempts_left=game_state.attempts_left,
        previous_words=[
            SimilarWordResponse(word=word.word, distance=word.distance)
            for word in sorted_words
        ],
        message=game_state.message,
        is_completed=game_state.is_completed,
        session_id=session_id
    )

@router.post("/game/start", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def start_new_game(
    request: Request, 
    response: Response,
    game_service: GameService = Depends(get_game_service)
):
    """Начинает новую игровую сессию.
    
    Создает новую сессию или переиспользует существующую на основе IP клиента.
    Возвращает состояние игры и session ID в теле ответа и заголовке X-Session-Id.
    """
    try:
        # Начинаем новую игру через сервис
        game_state, session_id = game_service.start_new_game(request.client.host)
        
        # Устанавливаем заголовок
        response.headers["X-Session-Id"] = session_id
        
        # Возвращаем ответ
        return _convert_game_state_to_response(game_state, session_id)
        
    except GameServiceError as e:
        logging.error(f"Service error in start_new_game: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании игры: {str(e)}"
        )
    except Exception as e:
        logging.error(f"Unexpected error in start_new_game: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Неожиданная ошибка при создании игры: {str(e)}"
        )

responses = {
    422: {"description": "Некорректное слово - слово не найдено в словаре, не является существительным или уже использовалось"},
    404: {"description": "Игра не найдена - начните новую игру"},
    409: {"description": "Игра уже завершена"},
    500: {"description": "Внутренняя ошибка сервера"}
}

@router.post("/game/guess", response_model=GameResponse, responses=responses)
async def make_guess(
    response: Response,
    guess: GuessRequest,
    session_id: str = Depends(validate_session),
    game_service: GameService = Depends(get_game_service)
):
    """Делает попытку угадать слово в текущей игре.
    
    Args:
        guess: Слово для угадывания (должно быть существительным)
        session_id: ID игровой сессии из заголовка X-Session-Id
    
    Returns:
        GameResponse с текущим состоянием игры
        
    Raises:
        422: Слово не найдено в словаре, не является существительным или уже использовалось
        404: Игра не найдена
        409: Игра уже завершена
        500: Ошибка сервера
    """
    try:
        # Получаем текущее состояние для проверки завершения
        current_state = game_service.get_game_state(session_id)
        
        if current_state.is_completed:
            response.status_code = status.HTTP_409_CONFLICT
            return _convert_game_state_to_response(current_state)
        
        # Делаем попытку через сервис
        game_state = game_service.make_guess(session_id, guess.word)
        
        # Проверяем результат и устанавливаем соответствующий статус
        if game_state.message and "Такого слова нет в словаре" in game_state.message:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        elif game_state.message and "Можно использовать только существительные" in game_state.message:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        elif game_state.message and "Это слово уже использовалось" in game_state.message:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        
        return _convert_game_state_to_response(game_state)
        
    except GameServiceError as e:
        if "Игра не найдена" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        elif "Игра уже завершена" in str(e):
            response.status_code = status.HTTP_409_CONFLICT
            current_state = game_service.get_game_state(session_id)
            return _convert_game_state_to_response(current_state)
        else:
            logging.error(f"Service error in make_guess: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка при обработке попытки: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in make_guess: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Неожиданная ошибка при обработке попытки: {str(e)}")

@router.get("/game/hint", response_model=GameResponse)
async def get_hint(
    response: Response,
    session_id: str = Depends(validate_session),
    game_service: GameService = Depends(get_game_service)
):
    """Получает подсказку для текущего слова."""
    try:
        # Получаем текущее состояние для проверки завершения
        current_state = game_service.get_game_state(session_id)
        
        if current_state.is_completed:
            response.status_code = status.HTTP_409_CONFLICT
            return _convert_game_state_to_response(current_state)

        # Получаем подсказку через сервис
        hint_message = game_service.get_hint(session_id)
        
        # Получаем обновленное состояние
        updated_state = game_service.get_game_state(session_id)
        
        return _convert_game_state_to_response(updated_state)
        
    except GameServiceError as e:
        if "Игра не найдена" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        elif "Игра завершена" in str(e):
            response.status_code = status.HTTP_409_CONFLICT
            current_state = game_service.get_game_state(session_id)
            return _convert_game_state_to_response(current_state)
        else:
            logging.error(f"Service error in get_hint: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка при получении подсказки: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in get_hint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Неожиданная ошибка при получении подсказки: {str(e)}")

