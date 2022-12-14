from Crypto.Hash import SHA256
from strgen import StringGenerator as SG
import random
import time
import string

sysrandom = random.SystemRandom()

def bincount(n):
    return bin(n).count("1")

def hash_task_one_ab():
    #random length for input string
    lth = sysrandom.randint(1, 16)
    #gernate a random string
    temp = SG("[\w\p]{"+str(lth)+"}").render()
    # print(temp + "\n")

    #caonvert string to int
    bits0 = int(temp.encode().hex(), 16)
    bitnum = sysrandom.randint(0, lth)
    #generate a string that is one bit different
    bits1 = bits0 ^ (1 << bitnum)
    print(bits0.to_bytes(lth, "big"))
    print(bits0.to_bytes(lth, "big"))
    #print hamming distance
    print(bincount(bits0 ^ bits1))
    print()

    #sha256 the two strings
    sha = SHA256.new()
    sha.update(bits0.to_bytes(lth, "big"))
    dig1 = sha.hexdigest()
    print(dig1)
    sha = SHA256.new()
    sha.update(bits1.to_bytes(lth, "big"))
    dig2 = sha.hexdigest()
    print(dig2)

#hash_task_one_ab()

def hash_task_one_c():
    col_found = False
    table = {}
    #len = 1
    start = time.time()
    for len in [1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 50]:
        while not col_found:
            #random length for input string
            lth = sysrandom.randint(1, 16)

            #gernate a random string
            res = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=lth))

            #do the hashing
            sha = SHA256.new()
            sha.update(res.encode())
            dig = (sha.hexdigest())[:13]

            #convert the digest to bin and int
            bits = bin(int(dig, 16))[2:(len+2)]
            key = int(bits, 2)

            #check the dictionary for collison
            if table.get(key) != None and table.get(key) != res:
                end = time.time()

                #hooray! collison found
                col_found = True
                # print(table.get(key))
                # print(temp)
                # print(bits)
                # print(key)
                print(end - start)

            #add key, string to dictionary
            else:
                table[key] = res
        col_found = False
        table.clear()

# print()
# for i in range(0,5):
#     hash_task_one_ab()
#     print()
hash_task_one_c()
