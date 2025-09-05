"""Day 30. Errors, Exceptions & JSON data"""

import random
import string
from tkinter import *
from tkinter import messagebox
from typing import Tuple
import json

MOST_COMMON_PASSWORDS = {
    '!ab#cd$', '000000', '00000000', '0000000000', '102030', '11111', '111111',
    '1111111', '11111111', '111111111', '1111111111', '111222tianya', '112233',
    '11223344', '121212', '123', '123123', '123123123', '123321', '1234',
    '12341234', '12344321', '12345', '123456', '123456!', '1234561',
    '123456123', '1234567', '12345678', '123456789', '1234567890',
    '1234567890123', '1234567891', '12345678910', '123456789a', '12345678Ab@',
    '123456a', '123456b', '123456c','123456d', '1234qwer', '123654',
    '123654789', '123abc', '123qwe', '12qwaszx', '1314520', '147258',
    '147258369', '159357', '159753', '1g2w3e4r', '1q2w3e', '1q2w3e4r',
    '1q2w3e4r5t', '1q2w3e4r5t1', '1qaz2wsx', '1qaz2wsx3edc', '1qaz2wsx3edc1',
    '1qazxsw2', '222222', '22535', '333333', '456789', '555555', '654321',
    '666666', '7758521', '777777', '7777777', '789456', '789456123',
    '87654321', '888888', '88888888', '987654', '987654321', '999999',
    'ABCDEF', 'Aa123456', 'Abcd1234', 'Abcd@1234', 'Daniel73!', 'Dragon',
    'Iloveyou', 'Indya123', 'Monkey', 'P@ssw0rd', 'Password', 'Password1',
    'Qwerty1', 'Qwerty1!', 'Qwerty12', 'Qwerty123', 'Qwerty123!', 'Qwerty1234',
    'Qwerty123?', 'Qwerty1?', 'Qwertyuiop', 'Samantha1', 'TimeLord12',
    'Welcome1', 'Welcome123', 'Welcome@123', 'a123456', 'a123456789',
    'aa123456', 'aaaaaa', 'aaaaaaaa', 'abc123', 'abcd1234', 'admin',
    'alexander', 'alphabet', 'amanda', 'amazon', 'andrea', 'andrew', 'android',
    'anthony', 'apple', 'asd123', 'asd123456', 'asdasd', 'asdf1234',
    'asdfasdf', 'asdfgh', 'asdfghjkl', 'ashley', 'asshole', 'azerty',
    'b123456', 'babygirl', 'baseball', 'basketball', 'batman', 'benjamin',
    'blink182', 'bmw', 'brandon', 'buster', 'butterfly', 'c123456', 'cambiami',
    'changeme','charlie', 'cheese', 'chelsea', 'chicken', 'chocolate',
    'chrome', 'computer', 'cookie', 'd123456', 'daniel', 'dearbook', 'diamond',
    'dragon', 'elon', 'facebook', 'family', 'flower', 'football', 'ford',
    'forever', 'freedom', 'fuckyou', 'fuckyou1', 'g_czechout', 'google',
    'gwerty', 'gwerty123', 'hannah', 'hello', 'hello123', 'hunter', 'iloveu',
    'iloveyou', 'iloveyou1', 'instagram', 'internet', 'iphone', 'jasmine',
    'jennifer', 'jessica', 'jonathan', 'jordan', 'jordan23', 'joseph',
    'joshua', 'jpmorgan', 'justin', 'killer', 'letmein', 'linux', 'liverpool',
    'lol123', 'love123', 'lovely', 'loveme', 'loveyou', 'macintosh', 'maggie',
    'master', 'matthew', 'michael', 'michael1', 'michelle', 'microsoft',
    'minecraft', 'monkey', 'mother', 'musk', 'mustang', 'myspace1', 'naruto',
    'netflix', 'nicole', 'nvidia', 'pakistan', 'passw0rd', 'password',
    'password1', 'password123', 'peanut', 'pepper', 'pokemon', 'princess',
    'princess1', 'purple', 'q1w2e3r4', 'q1w2e3r4t5y6', 'q1w2e3r4t5y61',
    'qazWSXedc123', 'qazwsx', 'qazwsxedc', 'qq123456', 'qwe123', 'qwer1234',
    'qwer4321', 'qwert', 'qwerty', 'qwerty1', 'qwerty12', 'qwerty123',
    'qwertyuiop', 'robert', 'samantha', 'samsung', 'secret', 'shadow',
    'soccer', 'starwars', 'summer', 'sunshine', 'superman', 'target123',
    'taylor', 'tesla', 'testing', 'thomas', 'tigger', 'tinkle', 'toyota',
    'trustno1', 'unknown', 'user', 'walmart', 'welcome', 'whatever',
    'whatsapp', 'william', 'windows', 'woaini', 'yellow', 'zag12wsx', 'zinch',
    'zuck', 'zxcvb', 'zxcvbnm',
}

def generate_password() -> str:
    """Generates password length in between 12-20 from unique and
    random characters.

    Returns
    -------
    str
        Generated password.
    """
    password = []
    # add random digits
    password += random.sample(string.digits, k=random.randint(3, 5))
    # add random lowercase letters
    password += random.sample(string.ascii_lowercase, k=random.randint(3, 5))
    # add random uppercase letters
    password += random.sample(string.ascii_uppercase, k=random.randint(3, 5))
    # add random special characters
    password += random.sample(string.punctuation, k=random.randint(3, 5))
    # randomly shuffle the password characters
    random.shuffle(password)
    return "".join(password)


def validate_password(username: str | int, pwd: str) -> Tuple[bool, str]:
    """Validates password according to the ruleset.

    Parameters
    ----------
    username : str | int
        Username/Email of the user.

    Returns
    -------
    Tuple[bool, str]
        Result & description message.
    """

    # 8-32 characters long
    if len(pwd) < 8 or len(pwd) > 32:
        return False, "Password must be 8-32 characters long"
    # at least one lowercase letter
    if not set(pwd).intersection(set(string.ascii_lowercase)):
        return False, "Password must include at least 1 lowercase letter."
    # at least one uppercase letter
    if not set(pwd).intersection(set(string.ascii_uppercase)):
        return False, "Password must include at least 1 uppercase letter."
    # at least one special character
    if not set(pwd).intersection(set(string.punctuation)):
        return False, "Password must include at least 1 special character."

    # must be different than previous five passwords (for this account)
    try:
        file = open("pass_data.json", "r", encoding="utf-8")
    except FileNotFoundError:
        pass
    else:
        # TODO Think Scalable: Reading large CSV/TSV file (chunk/batch/line/etc.),
        #   then also reading from down to top (reverse order).
        #   research: how to read large csv file (reverse order) in python
        #   https://stackoverflow.com/questions/17444679/
        #   https://stackoverflow.com/questions/260273/
        #   https://stackoverflow.com/questions/10933838/
        username_count = 0
        pass_data = json.load(file)
        for _, credentials in pass_data.items():
            if credentials["email"] == username:
                if credentials["password"].lower() == pwd.lower():
                    return (False, "Password must be different from your "
                            "previous five passwords (for this account).")
                username_count += 1
                if username_count > 5:
                    break
        file.close()        

    # must not match your user ID
    if str(username).lower() == pwd.lower():
        return False, "Password must not match your user ID"
    # must not include more than 2 identical characters
    # (for example: 111  or aaa)
    for i in range(len(pwd)):
        if i+2 < len(pwd) and pwd[i] == pwd[i+1] == pwd[i+2]:
            return (False, "Password must not contain more than 2 identical "
                    "characters in a row.")
    # must not include more than 2 consecutive characters:
    # (for example: 123 or abc)
    for i in range(len(pwd)):
        if i+2 < len(pwd) and (pwd[i] + pwd[i+1] + pwd[i+2]).isalnum():
            if ord(pwd[i]) + 2 == ord(pwd[i+1]) + 1 == ord(pwd[i+2]):
                return (False, "Password must not include more than 2 "
                        "consecutive characters.")
    # must not be a commonly used password (for example: password1)
    for pname in MOST_COMMON_PASSWORDS:
        if pname in pwd:
            return (False, "Password must not use a commonly used password.")

    return True, "OK"


def set_password():
    username = email_input.get().strip()
    if not username:
        messagebox.showwarning(message="Please enter the Email/Username.")
        return
    while True:
        new_pass = generate_password()
        if validate_password(username, new_pass)[0]:
            break
    password_input.delete(0, END)
    password_input.insert(0, new_pass)
    window.clipboard_clear()
    window.clipboard_append(new_pass)


def save_data():
    website = website_input.get().strip()
    username = email_input.get().strip()
    password = password_input.get().strip()
    if not all([website, username, password]):
        messagebox.showerror(message="Please don't leave any fields empty!")
        return
    check_pass = validate_password(username, password)
    if not check_pass[0]:
        messagebox.showwarning(title="Warning", message=check_pass[1])
        return
    confirmation = messagebox.askquestion(
        title="Confirmation",
        message=f"Username: {username}\nPassword: {password}\nIs this ok?"
    )
    if confirmation.lower() != "yes":
        return

    try:
        file = open("pass_data.json", "r", encoding="utf-8")
    except FileNotFoundError:
        pass_data = {}
    else:
        pass_data = json.load(file)
        file.close()

    pass_data.update({website: {"email": username, "password": password}})
    with open("pass_data.json", "w", encoding="utf-8") as file:
        json.dump(pass_data, file, indent=4)

    website_input.delete(0, END)
    password_input.delete(0, END)
    website_input.focus()


def search_website():
    website = website_input.get().strip()
    try:
        file = open("pass_data.json", "r", encoding="utf-8")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
        return
    else:
        pass_data = json.load(file)
        file.close()
        if website not in pass_data:
            messagebox.showerror(
                title="Error",
                message="No details for the website exists."
            )
            return
        website_credential = pass_data[website]
        messagebox.showinfo(
            title=website,
            message=f'Username: {website_credential["email"]}\n' \
                    f'Password: {website_credential["password"]}'
        )

# -------------------------- TKINTER GUI ------------------------------------ #
window = Tk()
window.title("Password Manager")
window.config(padx=35, pady=35)

lock_img = PhotoImage(file="logo.png")
lock_img_label = Label(image=lock_img)
lock_img_label.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, padx=15)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_input = Entry(width=21)
website_input.grid(row=1, column=1)
website_input.focus()

email_input = Entry(width=37)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "example@email.com")

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

search_btn = Button(text="Search", width=12, command=search_website)
search_btn.grid(row=1, column=2)

gen_pass_btn = Button(text="Generate Password", width=13, command=set_password)
gen_pass_btn.grid(row=3, column=2)

add_button = Button(text="Add", width=35, bg="blue", fg="white",
                    font=("", 10, "bold"), command=save_data)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
