import string
import random

import enchant
import difflib


class Corrector:
    def __init__(self, cities_path='russian_cities.txt', names_path='russian_names.txt'):
        self.cities_dict = enchant.PyPWL(cities_path)
        self.names_dict = enchant.PyPWL(names_path)

    def correct(self, woi, key, tresh_hold=0.6):

        if key == 'NAME':
            dictionary = self.names_dict
        elif key == 'CITY':
            dictionary = self.cities_dict
        elif key == 'LAST_NAME':
            return self.correct_last_name(woi)
        elif key == 'TEL':
            return self.correct_phone(woi)
        else:
            raise TypeError("wrong key name, only city/name")

        init_word = woi
        woi = ''.join(filter(str.isalpha, woi)).capitalize()
        sim = dict()

        suggestions = set(dictionary.suggest(woi))

        for word in suggestions:
            measure = difflib.SequenceMatcher(None, woi, word).ratio()
            sim[measure] = word

        if not suggestions or woi == 'Nan':
            return 1, init_word

        best_sim = max(sim.keys())

        if best_sim < tresh_hold:
            return 1, init_word
        else:
            return 0, sim[best_sim].capitalize()

    def correct_last_name(self, last_name):  # TODO
        f_last_nname = ''.join(filter(str.isalpha, last_name)).capitalize()
        if f_last_nname == 'Nan':
            return 1, last_name

        else:
            return 0, f_last_nname

    def correct_phone(self, number):
        f_number = ''.join(filter(str.isnumeric, str(number)))
        if len(f_number) != 7:
            return 1, number
        else:
            return 0, f_number


class SignUpGenerator:
    def __init__(self, pass_len=8):
        self.emails = set()
        self.PASSWORD_LENGTH = pass_len

    def generate_email(self, name, last_name):
        email = name[0] + '.' + last_name + "@companyname.com"
        if email in self.emails:
            email = name[:2] + '.' + last_name + "@companyname.com"
        self.emails.add(email)
        return email

    def generate_password(self):
        symbs = string.ascii_letters + string.digits + "-_*;^/"
        password = "".join(random.sample(symbs, self.PASSWORD_LENGTH))

        return password
