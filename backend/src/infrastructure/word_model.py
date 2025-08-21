import random
import logging
from typing import List
from src.domain.interfaces import IWordModel, SimilarWord
from src.model.connect import model, nlp

class WordModel(IWordModel):
    """Реализация интерфейса для работы с моделью слов"""
    
    def add_pos_tag(self, word: str) -> str:
        """Добавляет POS-тег к слову"""
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        if word.lower() in days:
            return f"{word}_PROPN"
        
        if word.endswith(('тельный', 'альный', 'яльный')):
            return f"{word}_ADJ"
        
        doc = nlp(word)
        pos = doc[0].pos_

        if pos == 'VERB' and word.endswith(('ный', 'ая', 'ое')):
            pos = 'ADJ'
        
        return f"{word}_{pos}"
    
    def get_random_word(self) -> str:
        """Получает случайное слово-существительное"""
        rand_word = random.choice(list(model.key_to_index.keys()))

        while self._checking_tag(rand_word.split("_")):
            logging.info(f"{rand_word} не удачно, добавляется {self.add_pos_tag(rand_word.split('_')[0]).split('_')[1]}")
            rand_word = random.choice(list(model.key_to_index.keys()))

        logging.info(rand_word)
        return rand_word
    
    def get_most_similar_word(self, target_word: str, guess_word: str) -> int:
        """Возвращает расстояние между двумя словами"""
        vocab = model.key_to_index
        target_idx = vocab.get(target_word)
        guess_idx = vocab.get(guess_word)
        
        if target_idx is None or guess_idx is None:
            logging.warning(f"Слово не найдено в словаре: target='{target_word}' ({target_idx}), guess='{guess_word}' ({guess_idx})")
            return 0
        
        return abs(target_idx - guess_idx)
    
    def get_most_similar_words(self, target_word: str, topn: int) -> List[SimilarWord]:
        """Возвращает список наиболее похожих слов с расстоянием в словаре"""
        similar_words_result = model.most_similar(positive=[target_word], topn=topn)
        return [
            SimilarWord(word=word[0].split('_')[0], distance=self.get_most_similar_word(target_word, word[0]))
            for word in similar_words_result
        ]
    
    def is_word_valid(self, word: str) -> bool:
        """Проверяет, есть ли слово в словаре"""
        return word in model.key_to_index
    
    def get_word_between(self, target_word: str, guess_word: str) -> str:
        """Возвращает слово, которое находится между двумя словами в словаре"""
        vocab = model.key_to_index
        
        # Получаем индексы слов
        target_idx = vocab.get(target_word)
        guess_idx = vocab.get(guess_word)
        
        if target_idx is None or guess_idx is None:
            # Если одно из слов не найдено, возвращаем случайное слово
            return self.get_random_word()
        
        # Вычисляем средний индекс
        middle_idx = (target_idx + guess_idx) // 2
        
        # Находим слово с ближайшим индексом
        closest_word = None
        min_distance = float('inf')
        
        for word, idx in vocab.items():
            distance = abs(idx - middle_idx)
            if distance < min_distance:
                min_distance = distance
                closest_word = word
        
        return closest_word or self.get_random_word()
    
    def _checking_tag(self, random_word_tag: list) -> bool:
        """Внутренний метод для проверки тега слова"""
        if self.add_pos_tag(random_word_tag[0]).split("_")[1] == random_word_tag[1] and random_word_tag[1] == "NOUN":
            return False
        return True
