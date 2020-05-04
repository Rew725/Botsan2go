import csv
from statistics import variance


def main():
    word = input()
    print(word_to_num(word))
    # 最適化のシード(チャンク化したワード)は4つ(右、左、逆右、逆左)
    left, right = chunking(word, word_to_num(word))
    re_right, re_left = chunking(word[::-1], word_to_num(word[::-1]))
    chunk_list = [left, right, re_left[::-1], re_right[::-1]]
    print(chunk_list)
    # シードを元に最適化
    optimizing_word = optimizing(chunk_list)
    print(optimizing_word)


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
    # 同指打鍵でチャンクが切れる理論が前提
    fingering_dict = get_fingering_dict()

    # 同指打鍵区切りにワードをリスト化
    # どのシードに対してもワードの数は等しくなる
    subword_list = []
    for i in range(len(chunk_list)):
        subword_list.append([])
        subword = ''
        for j in range(len(chunk_list[i])):
            if chunk_list[i][j] == '/':
                if fingering_dict[chunk_list[i][j - 1]] == fingering_dict[chunk_list[i][j + 1]]:
                    subword_list[i].append(subword)
                    subword = ''
                else:
                    subword += chunk_list[i][j]
            else:
                subword += chunk_list[i][j]
        subword_list[i].append(subword)
    
    # サブワード毎に最適化を行う
    ans = ''
    for i in range(len(subword_list[0])):
        point_list = []
        for j in range(len(subword_list)):
            point_list.append([])
            # チャンク数
            point_list[j].append(subword_list[j][i].count('/') + 1)
            # 分散
            sp = subword_list[j][i].split('/')
            data = []
            for s in sp:
                data.append(len(s))
            if len(data) == 1:
                point_list[j].append(0)
            else:
                point_list[j].append(round(variance(data), 2))
            # 末尾の子音の数
            cnt = 0
            for k in range(len(subword_list[j][i])):
                if subword_list[j][i][k] == '/':
                    if not is_vowel(subword_list[j][i][k - 1]):
                        cnt += 1
            if not is_vowel(subword_list[j][i][len(subword_list[j][i]) - 1]):
                cnt += 1
            point_list[j].append(cnt)
            # 番号
            point_list[j].append(j)
        point_list.sort()
        ans += '/' + subword_list[point_list[0][3]][i]
    ans = ans.lstrip('/')
    return ans


if __name__ == '__main__':
    main()
