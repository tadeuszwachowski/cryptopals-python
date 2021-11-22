import sb_xor

def main():
    best_match = ''
    best_score = 0
    best_key = ''
    with open('04.txt') as file:
        for line in file:
            match, score, key = sb_xor.brute_single_xor(line.strip())
            if score > best_score:
                best_match = match
                best_score = score
                best_key = key
    print(f"{best_key=}\n", best_match,  sep='')

if __name__ == "__main__":
    main()
