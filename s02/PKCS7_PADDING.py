def pkms(message,block_size):
    b = message.encode('ascii')
    diff = block_size - len(b)
    b += bytes([diff])*diff
    print(b)
        


def main():
    msg = "YELLOW SUBMARINE"
    block_size = 20
    
    pkms(msg,block_size)
    


if __name__ == '__main__':
    main()
