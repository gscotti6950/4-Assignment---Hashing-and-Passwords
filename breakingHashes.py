from pickle import NONE
from bcrypt import hashpw, checkpw
from nltk.corpus import words
import time
import concurrent.futures
from queue import Queue
from threading import Event
import random

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
    
        
def passwordCrackerFull(hash_string, codex_blocks, threads):

    event = Event()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
        futures = []
        for block in codex_blocks:
            futures.append(executor.submit(checkHashes, hash_string, block, event))
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                event.set()
                return future.result()
    return False

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
    print("making wordbanks...")
    hobbit = uniqueWords() #3350 words
    all_words = qualifiedWords(words.words()) #135145 words
    codex_blocks_hobbit = splitCodex(hobbit, 670)
    codex_blocks_all = splitCodex(all_words, 4)
    shadow_data = parseShadow()
    print("starting password craking...")
    for i in range (4):#(len(shadow_data)):
        current = "$" + shadow_data[i]["algorithm"] + "$" + shadow_data[i]["work_factor"] + "$" + shadow_data[i]["salt"]
        password = shadow_data[i]["hash_value"]
        hash_string = (current + password)
        start = time.time()
        print("checking hobbit...")
        found = passwordCrackerFull(hash_string, codex_blocks_hobbit, 4)
        if found:
            end = time.time()
            total_time = str((end-start))
            print(shadow_data[i]["name"] + " " + found + " | " + total_time)
        else:
            print("checking all words...")
            found = passwordCrackerFull(hash_string, codex_blocks_all, 4)
            end = time.time()
            total_time = str((end-start))
            print(shadow_data[i]["name"] + " " + found + " | " + total_time)

if __name__ == "__main__":
    main()