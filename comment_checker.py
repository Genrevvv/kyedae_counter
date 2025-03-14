from fuzzywuzzy import fuzz

import re


def check_kyedae_comment(string_comment):
    string_comment = string_comment.lower()
    string_comment = re.sub(r'[^a-zA-Z0-9\s]', ' ', string_comment)
    string_comment = string_comment.split()

    spellings = ["kyedae", "kyadae", "kaede"]

    substring = ""
    
    for spelling in spellings:

        for word in string_comment:
            #print(f"{word} : {spelling}")
            
            if word == spelling:
                return True
            elif fuzz.ratio(substring, spelling) >= 70 and substring.startswith("k"):
                print(f"\033[1mfuzz ratio: {fuzz.ratio(substring, spelling)}\033[0m")
                return True

    return False


def main():
    if check_kyedae_comment("iss_tthat..kaedep  from philipphines"):
        print("Kyedae comment FOUND")
    else:
        print("Kyedae comment NOT FOUND")


if __name__ == "__main__":
    main()
