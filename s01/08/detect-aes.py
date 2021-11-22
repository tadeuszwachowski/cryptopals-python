import binascii

def has_repeated_blocks(c,blocksize=16):
    # podziel tekst na bloki
    if len(c) % blocksize != 0:
        raise Exception('tekst nie jest podzielny przez dlugosc bloku')
    else:
        n_blocks = len(c) // blocksize

    blocks = [ c[i*blocksize:(i+1)*blocksize] for i in range(n_blocks) ]

    # sprawdz czy jakikolwiek blok sie powtarza
    if len(set(blocks)) != n_blocks:
        return True
    return False

with open('08.txt') as f:
    ciphertexts = [binascii.unhexlify(line.strip()) for line in f]

    hits = [c for c in ciphertexts if has_repeated_blocks(c)]

    for h in hits:
        print(h)

