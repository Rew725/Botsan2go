import chunk
import random_word

for i in random_word.get_random_word():
    word = i["romaji"]
    left, right = chunk.chunking(word, chunk.word_to_num(word))
    re_right, re_left = chunk.chunking(
        word[::-1], chunk.word_to_num(word[::-1]))
    chunk_list = [left, right, re_left[::-1], re_right[::-1]]
    print(i['kana']+"("+word+")")
    print(chunk.optimizing(chunk_list))
