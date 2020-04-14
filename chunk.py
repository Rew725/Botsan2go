import csv
import pprint
from statistics import variance

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

def is_vowel(char):
    if char == 'a' or char == 'i' or char == 'u' or char == 'e' or char == 'o':
        return True
    else:
        return False

def optimizing(chunk_list):
    fingering_dict = get_fingering_dict()
    subword = ''
    ans = ''
    left = []
    right = []
    re_left = []
    re_right = []
    # left
    for i in range(len(chunk_list[0])):
        if chunk_list[0][i] == '/':
            if fingering_dict[chunk_list[0][i - 1]] == fingering_dict[chunk_list[0][i + 1]]:
                left.append(subword)
                subword = ''
            else:
                subword += chunk_list[0][i]
        else:
            subword += chunk_list[0][i]
    left.append(subword)
    subword = ''
    # right
    for i in range(len(chunk_list[1])):
        if chunk_list[1][i] == '/':
            if fingering_dict[chunk_list[1][i - 1]] == fingering_dict[chunk_list[1][i + 1]]:
                right.append(subword)
                subword = ''
            else:
                subword += chunk_list[1][i]
        else:
            subword += chunk_list[1][i]
    right.append(subword)
    subword = ''
    # re_left
    for i in range(len(chunk_list[2])):
        if chunk_list[2][i] == '/':
            if fingering_dict[chunk_list[2][i - 1]] == fingering_dict[chunk_list[2][i + 1]]:
                re_left.append(subword)
                subword = ''
            else:
                subword += chunk_list[2][i]
        else:
            subword += chunk_list[2][i]
    re_left.append(subword)
    subword = ''
    # re_right
    for i in range(len(chunk_list[3])):
        if chunk_list[3][i] == '/':
            if fingering_dict[chunk_list[3][i - 1]] == fingering_dict[chunk_list[3][i + 1]]:
                re_right.append(subword)
                subword = ''
            else:
                subword += chunk_list[3][i]
        else:
            subword += chunk_list[3][i]
    re_right.append(subword)
    subword = ''
    print(left)
    print(right)
    print(re_left)
    print(re_right)
    left_point = []
    right_point = []
    re_left_point = []
    re_right_point = []
    for i in range(len(left)):
        # チャンク数
        left_point.append(left[i].count('/')+1)
        # 分散
        sp = left[i].split('/')
        data = []
        for s in sp:
            data.append(len(s))
        if len(data) == 1:
            left_point.append(0)
        else:
            left_point.append(variance(data))
        # 末尾の子音の数
        cnt = 0
        for j in range(len(left[i])):
            if left[i][j] == '/':
                if not is_vowel(left[i][j - 1]):
                    cnt += 1
        if not is_vowel(left[i][len(left[i]) - 1]):
            cnt += 1
        left_point.append(cnt)
        # 番号
        left_point.append(0)

        # チャンク数
        right_point.append(right[i].count('/')+1)
        # 分散
        sp = right[i].split('/')
        data = []
        for s in sp:
            data.append(len(s))
        if len(data) == 1:
            right_point.append(0)
        else:
            right_point.append(variance(data))
        # 末尾の子音の数
        cnt = 0
        for j in range(len(right[i])):
            if right[i][j] == '/':
                if not is_vowel(right[i][j - 1]):
                    cnt += 1
        if not is_vowel(right[i][len(right[i]) - 1]):
            cnt += 1
        right_point.append(cnt)
        # 番号
        right_point.append(1)

        # チャンク数
        re_left_point.append(re_left[i].count('/')+1)
        # 分散
        sp = re_left[i].split('/')
        data = []
        for s in sp:
            data.append(len(s))
        if len(data) == 1:
            re_left_point.append(0)
        else:
            re_left_point.append(variance(data))
        # 末尾の子音の数
        cnt = 0
        for j in range(len(re_left[i])):
            if re_left[i][j] == '/':
                if not is_vowel(re_left[i][j - 1]):
                    cnt += 1
        if not is_vowel(re_left[i][len(re_left[i]) - 1]):
            cnt += 1
        re_left_point.append(cnt)
        # 番号
        re_left_point.append(2)

        # チャンク数
        re_right_point.append(re_right[i].count('/')+1)
        # 分散
        sp = re_right[i].split('/')
        data = []
        for s in sp:
            data.append(len(s))
        if len(data) == 1:
            re_right_point.append(0)
        else:
            re_right_point.append(variance(data))
        # 末尾の子音の数
        cnt = 0
        for j in range(len(re_right[i])):
            if re_right[i][j] == '/':
                if not is_vowel(re_right[i][j - 1]):
                    cnt += 1
        if not is_vowel(re_right[i][len(re_right[i]) - 1]):
            cnt += 1
        re_right_point.append(cnt)
        # 番号
        re_right_point.append(3)

        print(left_point)
        print(right_point)
        print(re_left_point)
        print(re_right_point)

        point_list = []
        point_list.append(left_point)
        point_list.append(right_point)
        point_list.append(re_left_point)
        point_list.append(re_right_point)
        point_list.sort()
        
        if point_list[0][3] == 0:
            ans += '/' + left[i]
        if point_list[0][3] == 1:
            ans += '/' + right[i]
        if point_list[0][3] == 2:
            ans += '/' + re_left[i]
        if point_list[0][3] == 3:
            ans += '/' + re_right[i]

        left_point = []
        right_point = []
        re_left_point = []
        re_right_point = []
    return ans.lstrip('/')

# main--------------------
word = input()
print(word_to_num(word))
left, right = chunking(word, word_to_num(word))
re_right, re_left = chunking(word[::-1], word_to_num(word[::-1]))
chunk_list = [left, right, re_left[::-1], re_right[::-1]]
for l in chunk_list:
    print(l)
print(optimizing(chunk_list))
