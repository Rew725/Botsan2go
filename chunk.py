import csv
import pprint

def get_fingering_dict():
    # 運指表を辞書型で読み込む
    fingering_dict = {}
    with open('fingering.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            key, num = row[0].split('\t')
            fingering_dict[key] = num
    return fingering_dict

def word_to_num(word):
    # 運指表を辞書型で読み込む
    fingering_dict = {}
    with open('fingering.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            key, num = row[0].split('\t')
            fingering_dict[key] = num

    # wordを運指番号に変換する
    ans = []
    for key in word:
        ans.append(int(fingering_dict[key]))
    return ans

def chunking(word, num):
    chunk_word = ''
    chunk_num = ''
    is_hit_list = [0] * 10
    is_right_list = [1, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    is_right = is_right_list[num[0]]

    # 狭義のチャンク化
    for i in range(len(word)):
        if is_hit_list[num[i]] == 1 or is_right != is_right_list[num[i]]:
            # 同指打鍵または左右交互打鍵
            chunk_word += '/'
            chunk_num += '/'
            is_hit_list = [0] * 10
            is_right = is_right_list[num[i]]
        is_hit_list[num[i]] = 1
        chunk_word += word[i]
        chunk_num += str(num[i])

    # 広義のチャンク化
    # 左から右
    word_from_left = ''
    for i in range(len(chunk_word)):
        if chunk_word[i] == '/':
            if is_right_list[int(chunk_num[i - 1])] == 0 and is_right_list[int(chunk_num[i + 1])] == 1:
                continue
        # '/'でない時も'/'が条件を満たさない時も追加する
        word_from_left += chunk_word[i]
    # 右から左
    word_from_right = ''
    for i in range(len(chunk_word)):
        if chunk_word[i] == '/':
            if is_right_list[int(chunk_num[i - 1])] == 1 and is_right_list[int(chunk_num[i + 1])] == 0:
                continue
        # '/'でない時も'/'が条件を満たさない時も追加する
        word_from_right += chunk_word[i]

    # 同指打鍵の'/'でlist化して1.チャンク数が少ない方を選択2.分散が小さい方を選択3.末尾の子音が少ない方を選択
    return word_from_left, word_from_right

def optimizing(chunk_list):
    fingering_dict = get_fingering_dict()
    subword = ''
    ans = ''
    left = []
    right = []
    re_left = []
    re_right = []
    for i in range(len(chunk_list[0])):
        if chunk_list[0][i] == '/':
            if fingering_dict[chunk_list[0][i - 1]] == fingering_dict[chunk_list[0][i + 1]]:
                left.append(subword)
                subword = ''
            else:
                subword += chunk_list[0][i]
    # right
    # re_left
    # re_right
    return 3

# main--------------------
word = input()
print(word_to_num(word))
left, right = chunking(word, word_to_num(word))
re_right, re_left = chunking(word[::-1], word_to_num(word[::-1]))
chunk_list = [left, right, re_left[::-1], re_right[::-1]]
for l in chunk_list:
    print(l)