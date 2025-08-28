"""Day 24. Files, Directories, Paths"""

# Create a letter using starting_letter.txt 
with open("./Input/Letters/starting_letter.txt") as file:
    letter_template = file.read()

# for each name in invited_names.txt
for name in open("./Input/Names/invited_names.txt"):
    name = name.strip()
    file_name = f"letter_for_{name}.txt"
    with open(f"./Output/ReadyToSend/{file_name}", 'w') as file:
        # Replace the [name] placeholder with the actual name.
        file_data = letter_template.replace("[name]", name)
        # Save the letters in the folder "ReadyToSend".
        file.write(file_data)
        print(file_name)
