import logging
import uuid
import json
from typing import Optional, List
from src.database.connection import cursor
from src.domain.interfaces import IGameRepository, GameStats, GameState, SimilarWord

class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

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
            previous_words = []
            if row[2]:  # previous_words из БД
                try:
                    # Парсим JSON
                    if isinstance(row[2], str):
                        words_data = json.loads(row[2])
                    else:
                        words_data = row[2]
                    
                    for word_data in words_data:
                        if isinstance(word_data, dict):
                            previous_words.append(SimilarWord(
                                word=word_data["word"], 
                                distance=word_data["distance"]
                            ))
                except (json.JSONDecodeError, TypeError) as e:
                    logging.error(f"Ошибка парсинга previous_words: {e}")
                    # Возвращаем пустой список если не можем распарсить
                    previous_words = []
            
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
            
            # Ensure sessions row exists to satisfy FK constraint
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
            # Ensure column for client_ip exists (safe to run repeatedly)
            try:
                cursor.execute("ALTER TABLE sessions ADD COLUMN IF NOT EXISTS client_ip VARCHAR(255)")
            except Exception:
                # Some DB drivers may not support IF NOT EXISTS — ignore if fails
                pass

            if client_ip:
                cursor.execute("SELECT session_guid FROM sessions WHERE client_ip = %s", (client_ip,))
                row = cursor.fetchone()
                if row:
                    return str(row[0])

            session_guid = str(uuid.uuid4())
            # Insert with id=session_guid to satisfy existing schema (id is PK)
            cursor.execute(
                "INSERT INTO sessions (id, session_guid, client_ip) VALUES (%s, %s, %s)",
                (session_guid, session_guid, client_ip)
            )
            logging.info(f"Создана новая сессия {session_guid} for ip {client_ip}")
            return session_guid
        except Exception as e:
            logging.error(f"Ошибка создания сессии: {e}")
            raise DatabaseError(f"Не удалось создать сессию: {e}")

    def get_session_stats(self, session_id: str) -> GameStats:
        """Получает статистику для сессии"""
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_games,
                    SUM(CASE WHEN is_completed THEN 1 ELSE 0 END) as won_games,
                    AVG(CASE WHEN is_completed THEN attempts_left END) as avg_attempts
                FROM game_states
                WHERE session_id = %s
            """, (session_id,))
            row = cursor.fetchone()
            
            return GameStats(
                total_games=row[0] or 0,
                won_games=row[1] or 0,
                average_attempts=float(row[2]) if row[2] is not None else 0.0
            )
        except Exception as e:
            logging.error(f"Ошибка получения статистики: {e}")
            raise DatabaseError(f"Не удалось получить статистику: {e}")

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
