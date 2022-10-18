from bcrypt import hashpw, checkpw
import string


def uniqueWords():
    file = "./hobbit.txt"
    text = open(file, "r").readlines()
    split_text = []
    words = []

    for line in text:
        split_text.append(line.split(" "))

    for set in split_text:
        for word in set:
            words.append(word.translate(str.maketrans('', '', string.punctuation)).strip())

    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    print(len(unique_words))

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
    
def password_cracker(shadow_data):
    current = "$" + shadow_data[0]["algorithm"] + "$" + shadow_data[0]["work_factor"] + "$" + shadow_data[0]["salt"]
    hashed = hashpw(b"The", current.encode("utf-8"))
    password = b"The"

    if checkpw(password, hashed) == True:
        print("Password matches! The password is: " + password.decode("utf-8"))
    else:
        print("The passwords didn't match :(")
    
    #  print(hashpw(b"registrationsucks", current.encode("utf-8")))
    #  print(hashpw(b"registrationsucks", b"$2b$08$J9FW66ZdPI2nrIMcOxFYI."))
     


def main():
    # shadow_data = parseShadow()
    # print(shadow_data[0])
    # password_cracker(shadow_data)
    uniqueWords()

if __name__ == "__main__":
    main()