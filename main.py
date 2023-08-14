from random import choice
from string import punctuation, ascii_letters, digits


dictOfInfo = {}
listThatContainsEverything = list(digits + ascii_letters + punctuation)

while True:
    try:
        length = int(input("What's the length you want your password to be?"))
    except ValueError:
        print('You have typed wrong data type! Length has to be integer')
        continue

    password = ''.join([choice(listThatContainsEverything) for _ in range(length)])
    saveOrNot = input(f'{password}\nDo you want to use this password or generate a new one?(u - use and save, '
                      f'g - generate)').lower()
    if saveOrNot == 'u':

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

    elif saveOrNot == 'g':
        continue
    else:
        print('You typed wrong letter!')
        continue
