import string

# def scoretext(s):
#     score = 0
#     for letter in s:
#         if letter in string.ascii_letters or letter == " ":
#             score += 1
#     return score

def scoretext(input_bytes):
    input_bytes.encode('ASCII')
    # From https://en.wikipedia.org/wiki/Letter_frequency
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    ans = 0
    for byte in input_bytes:
        byte = byte.lower()
        try:
            ans += character_frequencies.get(byte, 0)
        except TypeError:
            pass
    return ans


def char_xor(s, key):
    b = bytes.fromhex(s)
    result = bytearray()
    key = ord(key)
    for char in b:
        result.append(char ^ key)
    # print(chr(key), result.decode('ascii'))
    return result.decode('ascii'), chr(key)


def brute_single_xor(inp):
    max_score = 0
    best_match = ""
    best_key = ""
    for c in string.printable:
        try:
            decrypted, key = char_xor(inp, c)
            score = scoretext(decrypted)
        except UnicodeDecodeError:
            score = 0
        if score > max_score:
            best_match = decrypted
            best_key = key
            max_score = score
    # print(best_key, best_match)
    return best_match, max_score, best_key




def main():
    inp = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    decoded, score, key = brute_single_xor(inp)
    print("Key: ", key)
    print("Plaintext: ", decoded)


if __name__ == "__main__":
    main()
