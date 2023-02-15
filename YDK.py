def open_ydk(filename: str):
    # Initialize an empty list to store the numbers
    numbers = []
    # Open the file
    with open(filename) as file:
        # Read each line in the file
        for line in file:
            # Remove leading and trailing whitespaces
            line = line.strip()
            # Skip the line if it starts with '#' (indicating a comment) or '!' (indicating the end of the file)
            if line.startswith('#') or line.startswith('!'):
                continue
            # Otherwise, add the number to the list
            numbers.append(int(line))

    # You can access the numbers stored in the list `numbers`
    print(numbers)
    return numbers




def create_ydk_log_file(id, string):
    filename = "Anime_cards/Logs.ydk"
    with open(filename, "a") as file:
        file.write(str(id) + "\n")
        file.write("#" + string + "\n")
    print("File created successfully!")
