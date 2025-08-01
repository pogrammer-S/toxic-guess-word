from scr.bot.bot_class import Game
from scr.model.connect import model

game = Game()

while True:
    message = input().lower()
    clean_word = game.add_pos_tag(message)
    #clean_word=message
    print(clean_word)

    if clean_word not in model.key_to_index:
        print(f"Слово '{message}' отсутствует в модели.")
    else:
        if clean_word == game.random_word:
            print(f"Вы победили за {game.tryers} попыток")
            game.random_word = game.new_random_word()
            game.old_messages = []
            game.tryers = 0
        else:
            if clean_word in game.old_messages:
                print("Это слово уже было")
            else:
                game.old_messages.append(clean_word)
                print(game.random_word)
                print(model.most_similar(positive=[game.random_word], negative=[clean_word], topn=3))
                game.tryers+=1
                