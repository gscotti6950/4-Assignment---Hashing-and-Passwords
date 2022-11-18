from Crypto.Hash import SHA256
from strgen import StringGenerator as SG
import random
import time
import string
import secrets

sysrandom = random.SystemRandom()

def method1():
    start = time.time()
    for i in range(100000):
        lth = sysrandom.randint(1, 16)
        #gernate a random string
        temp = SG("[\w\p]{"+str(lth)+"}").render()
    end = time.time()
    print(end - start)

def method2():
    start = time.time()
    for i in range(100000):
        lth = sysrandom.randint(1, 16)
        res = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=lth))
    end = time.time()
    print(end - start)

def method3():
    start = time.time()
    for i in range(100000):
        lth = sysrandom.randint(1, 16)
        res = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)for i in range(lth))
    end = time.time()
    print(end - start)

def testing():
    sizes = [1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 50]
    mask  = [1, 3, 15, 511, 8191, 131071, 1048575, 16777215, 268435455, 4294967295, 68719476735, 1099511627775, 17592186044415, 281474976710655, 1125899906842623]
    lth = sysrandom.randint(1, 16)
    res = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=lth))
    sha = SHA256.new()
    sha.update(res.encode())
    #dig = (sha.hexdigest())
    bits = sha.digest()
    num = int.from_bytes(bits, "big")
    temp  = num & 15
    print(temp)
    #print(len(bin(temp)))
    #binary = bin(int.from_bytes(bits, "big"))[2:]
    #print(len(bits))
    #print(len(binary))

testing()