from pickle import NONE
from bcrypt import hashpw, checkpw
from nltk.corpus import words
import time
import concurrent.futures
from queue import Queue
from threading import Event

#This function finds all of the unique values in hobbit.txt
def uniqueWords():
    file = "./hobbit.txt"
    split_text = open(file, "rb").read().decode('utf_8').split()
    words = []

    #now loop through the list of lists to get only one list
    for set in split_text:
        for word in set:
            if set.isalpha():
                words.append(set)
    
    #now loop through the list in order to find all of the unique words
    unique_words = []
    for word in words:
        if word.lower() not in unique_words and len(word) > 5 and len(word) < 11:
            unique_words.append(word.lower())
    return unique_words

def qualifiedWords(wordbank):
    uniqueWords = []
    for word in wordbank:
        if len(word) > 5 and len(word) < 11:
            uniqueWords.append(word.lower())
    return uniqueWords


#This function parses through shadow.txt
def parseShadow():
    file = "./shadow.txt"
    lines = open(file, "r").readlines()

    split_lines = []
    salt_split = []
    hash_value = []

    for line in lines:
        split_lines.append(line.split("$"))
    for line in split_lines:
        salt_split.append(line[-1][:22])
        hash_value.append((line[-1][22:]).strip())

    store = {}
    for i in range(len(split_lines)):
        store[i] = {
            "name": split_lines[i][0],
            "algorithm": split_lines[i][1],
            "work_factor": split_lines[i][2],
            "salt": salt_split[i],
            "hash_value": hash_value[i]
        }
    #print(store[1])
    return store
    
#This function hashes all of the unique words found by uniqueWords() an dcompares it to the hash value found in shadow.txt
def passwordCrackerHobbit(shadow_data, words):

    for i in range(len(shadow_data)):
        start_time = time.time()
        current = "$" + shadow_data[i]["algorithm"] + "$" + shadow_data[i]["work_factor"] + "$" + shadow_data[i]["salt"]
        password = shadow_data[i]["hash_value"]

        #iterate through all of the words
        for word in words:
            #checks if the hash of the current word matches the hash value from shadow.txt
            if checkpw(word.encode("utf-8"), (current+password).encode("utf-8")):#hashed[29:] == password:
                #hooray print password for the user
                print(shadow_data[i]["name"] + " " + word)
                found = True
                end_time = time.time()
                print("cracked in: ", (end_time - start_time))
                break

        #if the password was not found print sad statement
        if not found:
            passwordCrackerFull(shadow_data, i, start_time)
        
def passwordCrackerFull(shadow_data, i):

    current = "$" + shadow_data[i]["algorithm"] + "$" + shadow_data[i]["work_factor"] + "$" + shadow_data[i]["salt"]
    password = shadow_data[i]["hash_value"]
    print(current+password)
    hash_string = current+password
    codex_blocks = splitCodex((qualifiedWords(words.words())), 500)
    print(len(codex_blocks))
    print(shadow_data[i]["name"])
    print("done")

    event = Event()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = 40) as executor:
        futures = []
        for block in codex_blocks:
            futures.append(executor.submit(checkHashes, hash_string, block, event))
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                print(future.result())
                event.set()
    return None

def checkHashes(hash_temp, wordbank, event):
    for word in wordbank:
        if event.is_set():
            return
        if len(word) < 11 and len(word) > 5:
            if checkpw(word.encode("utf-8"), (hash_temp).encode("utf-8")):
                return word
    return False

def splitCodex(word_bank, n):
    #def chunks(lst, n):
    #"""Yield successive n-sized chunks from lst."""
    n = min(n, len(word_bank))
    k, m = divmod(len(word_bank), n)
    return list((word_bank[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)))

def main():
    shadow_data = parseShadow()
    # words = uniqueWords()
    # passwordCrackerHobbit(shadow_data, words)
    passwordCrackerFull(shadow_data, 4)

if __name__ == "__main__":
    main()