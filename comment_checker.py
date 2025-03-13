import re

from fuzzywuzzy import fuzz


def check_kyedae_comment(string_comment):
    string_comment = string_comment.lower()
    string_comment = re.sub(r'[^a-zA-Z0-9\s]', '', string_comment)

    spellings = ["kyedae", "kyadae", "kaede"]

    substring = ""
    
    for spelling in spellings:
        if string_comment.find(spelling) != -1:
            return True

        last_index = len(string_comment) - len(spelling)

        for i in range(last_index + 1):
            substring = string_comment[i:len(spelling) + i]                
            # print(f"{substring} : {spelling}")

            if fuzz.ratio(substring, spelling) >= 70:
                print(f"\033[1mfuzz ratio: {fuzz.ratio(substring, spelling)}\033[0m")
                return True

    # print("kyedae comment not detected")
    return False


def main():
    if check_kyedae_comment("kilala nio posi..kyeddae"):
        print("Kyedae comment FOUND")
    else:
        print("Kyedae comment NOT FOUND")


if __name__ == "__main__":
    main()
