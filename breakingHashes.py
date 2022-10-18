# import requests
from bcrypt import hashpw

# def uniqueWords(text):
#     unique_words = []
#     for word in text:
#         if word not in unique_words:
#             unique_words.append(word)
#     for x in unique_words:
#         print(x)

# hobbit_dir = "https://archive.org/stream/dli.ernet.474126/474126-The%20Hobbit%281937%29_djvu.txt"
# response = requests.get(hobbit_dir, "b")
# hobbit_text = response.text

# print(hobbit_text)



# password = b"super secret password"
# # Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(password, )
# # Check that an unhashed password matches one that has previously been
# # hashed
# if bcrypt.checkpw(password, hashed):
#     print("It Matches!")
# else:
#     print("It Does not Match :(")

# def myHash(text, salt):
#     print()



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
     print(hashpw(b"registrationsucks", current.encode("utf-8")))
     print(hashpw(b"registrationsucks", b"$2b$08$J9FW66ZdPI2nrIMcOxFYI."))



def main():
    shadow_data = parseShadow()
    print(shadow_data[0])
    password_cracker(shadow_data)



if __name__ == "__main__":
    main()