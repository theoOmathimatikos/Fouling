

def find_char_ind(text, n, find_char):

    count = 0
    for i, char in enumerate(text):
        if char == find_char:
            count += 1
            if count == n:
                return i
    return -1