import binascii
import base64
import string
import re
from operator import itemgetter

'''
IN: dwie wiadomosci, a i b
OUT: liczba rozniacych sie bitow (hamming distance)
'''
def hamming_dist(a,b):
    ans = ''.join( [bin(x^y)[2:] for x,y in zip(a,b)] )
    return ans.count("1")

'''
IN: zaszyfrowana wiadomosc
OUT: przewidywana dlugosc klucza
'''

def find_keysize(ciphertext):
    average_distances = []

    # Przewidywana dlugosc klucza, mozliwe do zmiany
    for keysize in range(2, 41):

        # lista do przechowywania Hamming distances dla tej dlugosci klucza
        distances = []

        # podziel tekst na bloki o dlugosci klucza
        chunks = [ciphertext[i:i+keysize]
                  for i in range(0, len(ciphertext), keysize)]

        while True:
            try:
                # oblicz hamming distance na podstawie dwoch pierwszych blokow
                chunk_1 = chunks[0]
                chunk_2 = chunks[1]
                distance = hamming_dist(chunk_1, chunk_2)

                # znormalizuj wynik dzielac przez dlugosc klucza
                # w ten sposob otrzymamy wynik z przedzialu [0,1]
                distances.append(distance/keysize)

                # usun te dwa bloki, zeby przy nie korzystac z nich
                # przy nastepnej iteracji
                del chunks[0]
                del chunks[1]

            # w przypadku wyjatku lub gdy wszystkie bloki zostaly juz przetworzone
            except Exception as e:
                break

        # dodaj dlugosc klucza wraz z jego wynikiem do pozostalych wynikow
        result = {
            'key': keysize,
            'avg distance': sum(distances) / len(distances)
        }
        average_distances.append(result)

    # wybierz najlepszy wynik
    possible_key_lengths = sorted(
        average_distances, key=lambda x: x['avg distance'])[0]
    return possible_key_lengths['key']

# from 04
def get_english_score(input_bytes):
    input_bytes.encode('ASCII')
    # https://en.wikipedia.org/wiki/Letter_frequency
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

def onecharxor(s, c):
    c = ord(c)
    return ''.join(map(lambda h: chr(ord(h) ^ c), s))

def xorcharbrute(s):
    scores = {}
    for key in string.printable:
        result = onecharxor(s, key)
        pretty_result = re.sub(r'[\x00-\x1F]+', '', result)
        if pretty_result != '':
            points = get_english_score(pretty_result)
            scores[points] = [pretty_result, key]
            # print(f"{key}: {pretty_result}")

    top_keys = sorted(scores.keys(), reverse=True)[:5]
    # for tk in top_keys:
    #     print(scores[tk])
    # return scores[top_keys[0]]
    return scores[top_keys[0]][1]

def xorbrutepass(text):
    keylen = find_keysize(text)
    blocks = [[] for _ in range(keylen)]
    # print(blocks)
    for c in range(len(text)):
        ind = c % keylen
        blocks[ind].append(text[c:c+1])
    # print(blocks)
    # print(len(blocks))

    potential_pass = ''

    for bk in blocks:
        # print(b''.join(bk))
        potential_pass += xorcharbrute(b''.join(bk).decode('ascii'))
    # print(keylen, potential_pass)
    return potential_pass

def xordecode(ciphertext,key):
    keylen = len(key)
    plaintext = ''
    for i in range(len(ciphertext)):
        ind = i % keylen
        plaintext += chr(ord(key[ind]) ^ ciphertext[i])
    # plaintext = plaintext.encode('ascii').hex()
    print(plaintext)
    return plaintext

def main():
    # a = "this is a test"
    # b = "wokka wokka!!!"
    # print(hamming_dist(a,b))

    with open('06.txt') as f:
        message = ''.join(f.read().splitlines())
    text = base64.b64decode(message)
    password = xorbrutepass(text)
    print("Password: ",password, "\n")
    xordecode(text,password)

if __name__ == '__main__':
    main()
