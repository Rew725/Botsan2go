import json
import random
with open('word_list.json', 'r') as f:
    json_load = json.load(f)
    word_list = json_load['joyo']['word']
    randnum = random.randint(1, len(word_list))
    random_word = [word_list[randnum-1],
                   word_list[randnum], word_list[randnum+1]]
    print(random_word)
