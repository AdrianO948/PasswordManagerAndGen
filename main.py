from random import choice
from string import punctuation, ascii_letters, digits
import re
from cryptography.fernet import Fernet


dictOfInfo = {}
listOfEveryCharacter = list(digits + ascii_letters + punctuation)
flag = True
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
key = Fernet.generate_key()
fernet = Fernet(key)
file = 'password.txt'


def generate_password(list_of_characters):
    passw = ''.join([choice(list_of_characters) for _ in range(length)])
    return passw


def choose_abort_generate_or_use(passw):
    select = input(f'{passw}\nDo you want to use this password or generate a new one?(u - use and save, '
                   f'g - generate, y - abort)').lower()
    return select


def options_statement():
    input_letter = input("Press any digit to start or 'q' button if you want to exit "
                         "or 'r' if you want to check your passwords: ")
    if input_letter == 'q':
        return False

    elif input_letter == 'r':
        list_of_read_content = reading_out_of_file(file)
        new_output_list = []

        for item in list_of_read_content:
            item = item.split(': ')
            new_output_list.append(item)

        for item in new_output_list:
            if 'site' in item:
                print(f"{item[1]}")

        site_number = int(input('To which site do you want to check password? Pass site number: '))
        print(new_output_list[site_number * 4 - 4][1])
        email_address = input('Pass the email address connected to this account: ')
        key_read = new_output_list[0][1]
        key_read.encode()
        new_fernet = Fernet(key_read)
        email_position = new_output_list[site_number * 4 - 2][1]
        passw_position = new_output_list[site_number * 4 - 1][1]
        decrypted_email = new_fernet.decrypt(email_position).decode()
        decrypted_password = new_fernet.decrypt(passw_position).decode()

        if email_address == decrypted_email:
            print(f'Correct email.\nThe password: {decrypted_password}')

    else:
        return True


def reading_out_of_file(file_name):
    with open(file_name, 'r')as file_read:
        list_of_content = file_read.readlines()
    return list_of_content


while flag:

    flag = options_statement()
    if not flag:
        break

    try:
        length = int(input("What's the length you want your password to be?: "))
    except ValueError:
        print('You have typed wrong data type! Length has to be integer')
        continue

    password = generate_password(listOfEveryCharacter)
    selection = choose_abort_generate_or_use(password)

    if selection == 'u':
        while True:
            email = input('Pass your e-mail address: ')
            if not re.fullmatch(regex, email):
                print('Wrong email!')
                continue

            site = input("Enter the site url for which this password is gonna be: ")

            if not site.startswith('https://') or site.startswith('http://'):
                site = 'https://' + site

            encEmail = fernet.encrypt(email.encode())
            encPassword = fernet.encrypt(password.encode())
            dictOfInfo[site] = [encEmail, encPassword]

            try:
                with open(file, 'a+')as f:
                    for site, mailAndPasswordList in dictOfInfo.items():
                        stringToWrite = (f'key: {key.decode()}\nsite: {site}\nemail: {mailAndPasswordList[0].decode()}'
                                         f'\npassword: {mailAndPasswordList[1].decode()}\n')
                        f.write(stringToWrite)
                    del dictOfInfo[site]

            except FileNotFoundError:
                with open(file, 'w')as f:
                    for site, mailAndPasswordList in dictOfInfo.items():
                        stringToWrite = (f'key: {key.decode()}\nsite: {site}\nemail: {mailAndPasswordList[0].decode()}'
                                         f'\npassword: {mailAndPasswordList[1].decode()}\n')
                        f.write(stringToWrite)
                    del dictOfInfo[site]
            break

    elif selection == 'g':
        continue

    elif selection == 'y':
        break

    else:
        print('You typed wrong letter!')
        continue
