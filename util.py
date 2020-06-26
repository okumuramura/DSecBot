import re

def check_words_correct(word, target):
    def distance(a, b):
        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    word = word.lower()
    target = target.lower()
    word = re.sub("\s*\(.*\)", "" , word)
    target = re.sub("\s*\(.*\)", "", target)
    almost = False
    if re.search("((\s+)|(^)){0}((\s+)|($))".format(word), target):
        almost = True
    dist = distance(re.sub("\s", "", word), re.sub("\s", "", target))

    if 1 <=  dist <= 2:
        return 0
    elif dist == 0:
        return 2
    else:
        if almost:
            return 1
        else:
            return -1


def gen_hp(Emoji, id, hp):
    return "<@!{0}>'s HP: ".format(id) + "".join(([Emoji.heartfull] * (hp // 2)) + ([Emoji.hearthalf] * (hp % 2)) + ([Emoji.heartno] * (5 - hp//2 - hp%2)))
