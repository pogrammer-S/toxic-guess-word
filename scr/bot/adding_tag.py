from scr.model.connect import nlp

def add_pos_tag(word):
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    if word.lower() in days:
        return f"{word}_PROPN"
    
    # на -тельный
    if word.endswith(('тельный', 'альный', 'яльный')):
        return f"{word}_ADJ"
    
    doc = nlp(word)
    pos = doc[0].pos_

    if pos == 'VERB' and word.endswith(('ный', 'ая', 'ое')):
        pos = 'ADJ'
    
    return f"{word}_{pos}"