import sys

import pandas as pd

from tools import *


def correct_data(table_name='task_file.txt'):

    df = pd.read_csv(table_name, sep=',', index_col=False).astype(str)

    corrector = Corrector()

    df["WRONG_NAME"] = df["NAME"].apply(lambda x: corrector.correct(x, "NAME"))
    df["NAME"] = df["WRONG_NAME"].apply(lambda x: x[1])
    df["WRONG"] = df["WRONG_NAME"].apply(lambda x: x[0])

    df["WRONG_LAST_NAME"] = df["LAST_NAME"].apply(
        lambda x: corrector.correct(x, "LAST_NAME"))
    df["LAST_NAME"] = df["WRONG_LAST_NAME"].apply(lambda x: x[1])
    df["WRONG"] += df["WRONG_LAST_NAME"].apply(lambda x: x[0])

    df["WRONG_TEL"] = df["TEL"].apply(lambda x: corrector.correct(x, "TEL"))
    df["TEL"] = df["WRONG_TEL"].apply(lambda x: x[1])
    df["WRONG"] += df["WRONG_TEL"].apply(lambda x: x[0])

    df["WRONG_CITY"] = df["CITY"].apply(lambda x: corrector.correct(x, "CITY"))
    df["CITY"] = df["WRONG_CITY"].apply(lambda x: x[1])
    df["WRONG"] += df["WRONG_CITY"].apply(lambda x: x[0])

    df = df.drop_duplicates()

    correct_df = df[df.WRONG == 0][[
        'EMAIL', 'NAME', 'LAST_NAME', 'TEL', 'CITY']]
    incorrect_df = df[df.WRONG == 1]

    su_gen = SignUpGenerator()

    correct_df[['EMAIL', 'PASSWORD']] = correct_df[['NAME', 'LAST_NAME']].apply(lambda x: pd.Series(
        [su_gen.generate_email(x['NAME'], x['LAST_NAME']), su_gen.generate_password()]), axis=1)

    correct_df.to_csv('correct_df.csv', index=False)
    incorrect_df.to_csv('incorrect_df.csv', index=False)

    print(
        f'Correct lines: {correct_df.shape[0]}\nIncorrect lines: {incorrect_df.shape[0]}')


def online_correct(table_name='correct_df.csv'):
    name, last_name, phone, city = input('Enter name: '), input(
        'Enter last_name: '), input('Enter phone: '), input('Enter city: ')


    corrector = Corrector()

    while True:
        error, sugg_name = corrector.correct(name, "NAME")
        if error == 1:
            name = input("Name is not recognized, try again: ")
        elif error == 2:
            opt = int(
                input(f"Bad name, suggested name: {sugg_name}, save this name? (1/0): "))
            if opt == 1:
                name = sugg_name
                break
            else:
                name = input('Input name: ')
                break
        elif error == 0:
            name = sugg_name
            break

    while True:
        error, sugg_name = corrector.correct(last_name, "LAST_NAME")
        if error == 1:
            name = input("Last name is not recognized, try again: ")
        elif error == 0:
            last_name = sugg_name
            break

    while True:
        error, sugg_name = corrector.correct(phone, "TEL")
        if error == 1:
            phone = input("Phone number is incorrect, try again: ")
        elif error == 0:
            phone = sugg_name
            break

    while True:
        error, sugg_name = corrector.correct(city, "CITY")
        if error == 1:
            city = input("City is not recognized, try again: ")
        elif error == 2:
            opt = int(
                input(f"Bad city name, suggested name: {sugg_name}, save this city? (1/0): "))
            if opt == 1:
                city = sugg_name
                break
            else:
                city = input('Enter city: ')
                break
        elif error == 0:
            city = sugg_name
            break

    su_gen = SignUpGenerator()

    email = su_gen.generate_email(name, last_name)
    password = su_gen.generate_password()

    df = pd.DataFrame({'EMAIL': [email], 'NAME': [name], 'LAST_NAME': [last_name],
                      'TEL': [phone], 'CITY': [city], 'PASSWORD': [password]})
                    

    print('Created user:')
    print(df)

    full_df = pd.read_csv(table_name)
    pd.concat([full_df, df], ignore_index=True).to_csv(table_name, index=False)
