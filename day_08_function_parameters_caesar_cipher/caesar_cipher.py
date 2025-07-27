"""DAY 8. CAESAR CIPHER."""

CAESAR_CIPHER_ART = r'''
 ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,  
a8"     "" ""     `Y8 a8P_____88 I8[    "" ""     `Y8 88P'   "Y8  
8b         ,adPPPPP88 8PP"""""""  `"Y8ba,  ,adPPPPP88 88          
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88          
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88

           88             88                                 
           ""             88                                 
                          88                                 
 ,adPPYba, 88 8b,dPPYba,  88,dPPYba,   ,adPPYba, 8b,dPPYba,  
a8"     "" 88 88P'    "8a 88P'    "8a a8P_____88 88P'   "Y8  
8b         88 88       d8 88       88 8PP""""""" 88          
"8a,   ,aa 88 88b,   ,a8" 88       88 "8b,   ,aa 88          
 `"Ybbd8"' 88 88`YbbdP"'  88       88  `"Ybbd8"' 88          
              88                                             
              88
'''

print(CAESAR_CIPHER_ART)

def caesar_cipher(message: str, shift_key: int, option: str) -> str:
    """Encrypts/Decrypts message according to the shift number."""
    result = ""
    if option == "decode":
        shift_key *= -1
    for char in message.lower():
        if char.isalpha():
            result += chr((ord(char) - 97 + shift_key) % 26 + 97)
        else:
            result += char
    return result


def main():

    while True:
        cipher_option = input(
            "Type 'encode' to encrypt, type 'decode' to decrypt: "
        ).strip().lower()
        msg = input("Enter your message:\n")
        key = int(input("Enter the shift number: "))

        result_msg = caesar_cipher(msg, key, cipher_option)
        print(f"{cipher_option.upper()}D RESULT:\n{result_msg}")

        go_again = input("\nTry again? [yes/no]: ").strip().lower()
        if go_again in ["yes", "y"]:
            continue
        print("Goodbye!")
        break


if __name__ == "__main__":
    main()
