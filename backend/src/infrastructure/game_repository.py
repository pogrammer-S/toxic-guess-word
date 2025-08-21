import logging
import uuid
import json
from typing import Optional, List
from src.database.connection import cursor
from src.domain.interfaces import IGameRepository, GameState, SimilarWord
from src.application.game_service import WordParser, DatabaseError

class GameRepository(IGameRepository):
    """Реализация интерфейса для работы с состоянием игры в БД"""
    
    def get_game_state(self, session_id: str) -> Optional[GameState]:
        """Получает текущее состояние игры для сессии"""
        try:
            cursor.execute("""
                SELECT target_word, attempts_left, previous_words, is_completed
                FROM game_states
                WHERE session_id = %s
                ORDER BY created_at DESC
                LIMIT 1
            """, (session_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
                
            # Преобразуем previous_words из БД в список SimilarWord
            previous_words = WordParser.parse_previous_words(row[2])
            
            return GameState(
                target_word=row[0],
                attempts_left=row[1],
                previous_words=previous_words,
                is_completed=row[3],
                session_id=session_id
            )
        except Exception as e:
            logging.error(f"Ошибка получения состояния игры: {e}")
            raise DatabaseError(f"Не удалось получить состояние игры: {e}")

    def save_game_state(self, game_state: GameState) -> None:
        """Сохраняет состояние игры"""
        try:
            # Преобразуем SimilarWord в JSON строку для БД
            previous_words_db = json.dumps([
                {"word": word.word, "distance": word.distance}
                for word in game_state.previous_words
            ])
            
            # Обеспечиваем существование строки сессии для удовлетворения FK ограничения
            self._ensure_session_exists(game_state.session_id)
            
            cursor.execute("""
                INSERT INTO game_states (
                    session_id, target_word, attempts_left, previous_words, is_completed
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                game_state.session_id, 
                game_state.target_word, 
                game_state.attempts_left, 
                previous_words_db,
                game_state.is_completed
            ))
            logging.info(f"Создано новое состояние игры для сессии {game_state.session_id}")
        except Exception as e:
            logging.error(f"Ошибка сохранения состояния игры: {e}")
            raise DatabaseError(f"Не удалось сохранить состояние игры: {e}")

    def create_session(self, client_ip: Optional[str] = None) -> str:
        """Создает новую сессию и возвращает её id"""
        try:
            if client_ip:
                cursor.execute("SELECT session_guid FROM sessions WHERE client_ip = %s", (client_ip,))
                row = cursor.fetchone()
                if row:
                    return str(row[0])

            session_guid = str(uuid.uuid4())
            # Вставляем с id=session_guid для удовлетворения существующей схемы (id является PK)
            cursor.execute(
                "INSERT INTO sessions (id, session_guid, client_ip) VALUES (%s, %s, %s)",
                (session_guid, session_guid, client_ip)
            )
            logging.info(f"Создана новая сессия {session_guid} для IP {client_ip}")
            return session_guid
        except Exception as e:
            logging.error(f"Ошибка создания сессии: {e}")
            raise DatabaseError(f"Не удалось создать сессию: {e}")



    def _ensure_session_exists(self, session_id: str) -> None:
        """Обеспечивает существование сессии в БД"""
        try:
            cursor.execute("SELECT 1 FROM sessions WHERE id = %s", (session_id,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO sessions (id) VALUES (%s)", (session_id,))
                logging.info(f"Создана новая сессия с id {session_id}")
        except Exception as e:
            logging.error(f"Ошибка при создании/проверке сессии: {e}")
            raise DatabaseError(f"Не удалось создать/проверить сессию: {e}")
