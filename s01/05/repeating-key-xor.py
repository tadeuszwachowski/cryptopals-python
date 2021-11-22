import binascii
# message = input("Paste the message:\n")
message = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
message_b = bytes(message, 'ascii')
key = "ICE"
keylen = len(key)

ciphertext = ''
for i in range(len(message_b)):
    ind = i % keylen
    ciphertext += chr(ord(key[ind]) ^ ord(message[i]))
ciphertext = ciphertext.encode('ascii').hex()
print(ciphertext)
