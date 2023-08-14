from random import choice
from string import punctuation, ascii_letters, digits


dictOfInfo = {}
listOfEveryCharacter = list(digits + ascii_letters + punctuation)


def generate_password(list_of_characters):
    passw = ''.join([choice(list_of_characters) for _ in range(length)])
    return passw


def choose_abort_generate_or_use(passw):
    select = input(f'{passw}\nDo you want to use this password or generate a new one?(u - use and save, '
                      f'g - generate, y - abort)').lower()
    return select


while True:
    try:
        length = int(input("What's the length you want your password to be?(Y to abort)"))
    except ValueError:
        print('You have typed wrong data type! Length has to be integer')
        continue

    password = generate_password(listOfEveryCharacter)
    selection = choose_abort_generate_or_use(password)

    if selection == 'u':

        mail = input('Pass your e-mail address: ')
        site = input("Enter the site url for which this password is gonna be: ")
        if site.startswith('https://'):
            pass
        else:
            site = 'https://' + site

        dictOfInfo[site] = [mail, password]

        try:
            with open('password.txt', 'a+')as f:
                for site, mailAndPasswordList in dictOfInfo.items():
                    stringToWrite = f'site: {site}\nmail: {mailAndPasswordList[0]}\npassword: {mailAndPasswordList[1]}\n'
                    f.write(stringToWrite)
                del dictOfInfo[site]

        except FileNotFoundError:
            with open('password.txt', 'w')as f:
                for key, value in dictOfInfo.items():
                    stringToWrite = f'site: {key}\nmail: {value[0]}\npassword: {value[1]}\n'
                    f.write(stringToWrite)

    elif selection == 'g':
        continue
    elif selection == 'y':
        break
    else:
        print('You typed wrong letter!')
        continue
