import random
from scr.model.connect import model
from scr.bot.adding_tag import add_pos_tag

global random_word, tryers, old_meessages

def checking_tag(random_word_tag:list):
    if add_pos_tag(random_word_tag[0]).split("_")[1] == random_word_tag[1]:
        return False
    return True

def start_game():
    global random_word, tryers, old_meessages
    random_word = random.choice(list(model.key_to_index.keys()))
    while checking_tag(random_word.split("_")):
        print(f"{random_word} не удачно, добавляется {add_pos_tag(random_word.split('_')[0]).split('_')[1]}")
        random_word = random.choice(list(model.key_to_index.keys()))
        
    tryers=0
    old_meessages=[]
    print(random_word)

start_game()

