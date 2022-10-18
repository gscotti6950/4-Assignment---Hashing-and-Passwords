from bcrypt import hashpw, checkpw
import string

#This function finds all of the unique values in hobbit.txt
def uniqueWords():
    file = "./hobbit.txt"
    text = open(file, "r").readlines()
    split_text = []
    words = []

    #loop through text to get words into list
    for line in text:
        split_text.append(line.split(" "))

    #now loop through the list of lists to get only one list
    for set in split_text:
        for word in set:
            #get rid of any alphanumeric values
            words.append(word.translate(str.maketrans('', '', string.punctuation)).strip())
    
    #now loop through the list in order to find all of the unique words
    unique_words = []
    for word in words:
        if word not in unique_words and len(word) > 5 and len(word) < 11:
            unique_words.append(word)
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
    return store
    
#This function hashes all of the unique words found by uniqueWords() an dcompares it to the hash value found in shadow.txt
def password_cracker(shadow_data, words):

    current = "$" + shadow_data[0]["algorithm"] + "$" + shadow_data[0]["work_factor"] + "$" + shadow_data[0]["salt"]
    password = shadow_data[0]["hash_value"]

    #iterate through all of the words
    for word in words:
        #hash the current word
        hashed = hashpw(word.encode("utf-8"), current.encode("utf-8"))[29:]

        # if checkpw(password, hashed) == True:
        #     print(shadow_data[0]["name"] + " " + word)

        #checks if the hash of the current word matches the hash value from shadow.txt
        if hashed == password:
            #hooray print password for the user
            print(shadow_data[0]["name"] + " " + word)
        # else:
        #     print("Word tried: " + word)
        #     print("Hashed Value: " + password)
        #     print("Current Hash Value: " + hashed.decode("utf-8"))

    #if the password was not found print sad statement
    print("password not found :(")


def main():
    shadow_data = parseShadow()
    words = uniqueWords()
    password_cracker(shadow_data, words)
    

if __name__ == "__main__":
    main()