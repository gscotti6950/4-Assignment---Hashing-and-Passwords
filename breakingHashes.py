#from curses.ascii import isalnum
from bcrypt import hashpw, checkpw
from nltk.corpus import words
import string
import re

#This function finds all of the unique values in hobbit.txt
def uniqueWords():
    file = "./hobbit.txt"
    split_text = open(file, "rb").read().decode('utf_8').split()
    #split_text = []
    words = []

    #loop through text to get words into list
    # for line in text:
    #     split_text.append(line.split(" "))

    #now loop through the list of lists to get only one list
    for set in split_text:
        for word in set:
            #get rid of any alphanumeric values
            #words = [t for t in split_text if re.match(r'[^\W\d]*$', t)]
            if set.isalpha():
                words.append(set)
    
    #now loop through the list in order to find all of the unique words
    unique_words = []
    for word in words:
        if word.lower() not in unique_words and len(word) > 5 and len(word) < 11:
            unique_words.append(word.lower())
    print(len(unique_words))
    return unique_words

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
def password_cracker_hobbit(shadow_data, words):
    i = 4
    found = False

    current = "$" + shadow_data[i]["algorithm"] + "$" + shadow_data[i]["work_factor"] + "$" + shadow_data[i]["salt"]
    password = shadow_data[i]["hash_value"]
    print(current+password)

    #iterate through all of the words
    #passw = hashpw(b"hobbit", current.encode("utf-8"))
    for word in words:
        #hash the current word
        #hashed = (hashpw(word.encode("utf-8"), current.encode("utf-8")))

        # if checkpw(password, hashed) == True:
        #     print(shadow_data[0]["name"] + " " + word)

        #checks if the hash of the current word matches the hash value from shadow.txt
        if checkpw(word.encode("utf-8"), (current+password).encode("utf-8")):#hashed[29:] == password:
            #hooray print password for the user
            print(shadow_data[i]["name"] + " " + word)
            found = True
            break
        # else:
        #     print("Word tried: " + word)
        #     print("Hashed Value: " + password)
        #     print("Current Hash Value: " + hashed.decode("utf-8"))

    #if the password was not found print sad statement
    if not found:
        password_cracker_full(shadow_data, i)
        
def password_cracker_full(shadow_data, thingy):
    found = False
    i = thingy

    current = "$" + shadow_data[i]["algorithm"] + "$" + shadow_data[i]["work_factor"] + "$" + shadow_data[i]["salt"]
    password = shadow_data[i]["hash_value"]
    print(current+password)

    #iterate through all of the words
    #passw = hashpw(b"hobbit", current.encode("utf-8"))
    for word in words.words():
        #hash the current word
        #hashed = (hashpw(word.encode("utf-8"), current.encode("utf-8")))

        # if checkpw(password, hashed) == True:
        #     print(shadow_data[0]["name"] + " " + word)

        #checks if the hash of the current word matches the hash value from shadow.txt
        if len(word) < 11 or len(word) > 5:
            if checkpw(word.encode("utf-8"), (current+password).encode("utf-8")):#hashed[29:] == password:
            #hooray print password for the user
                print(shadow_data[i]["name"] + " " + word)
                found = True
                break
        # else:
        #     print("Word tried: " + word)
        #     print("Hashed Value: " + password)
        #     print("Current Hash Value: " + hashed.decode("utf-8"))

    #if the password was not found print sad statement
    if not found:
        print("No password found >:(")


def main():
    shadow_data = parseShadow()
    #words = uniqueWords()
    #password_cracker_hobbit(shadow_data, words)
    password_cracker_full(shadow_data, 4)
    # test()
    

if __name__ == "__main__":
    main()