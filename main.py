from scr.bot.adding_tag import add_pos_tag
from scr.model.connect import model
from scr.bot.start_game import start_game
import scr.bot.start_game as sg
import random
global random_word, tryers, old_meessages

while True:
    message = input().lower()
    clean_word = add_pos_tag(message)
    #clean_word=message
    print(clean_word)

    if clean_word not in model.key_to_index:
        print(f"Слово '{message}' отсутствует в модели.")
    else:
        if clean_word == sg.random_word:
            print(f"Вы победили за {sg.tryers} попыток")
            start_game()
        else:
            if clean_word in sg.old_meessages:
                print("Это слово уже было")
            else:
                sg.old_meessages.append(clean_word)
                print(sg.random_word)
                print(model.most_similar(positive=[sg.random_word], negative=[clean_word], topn=3))
                sg.tryers+=1
                