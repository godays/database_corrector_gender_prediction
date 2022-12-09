import sys

import data_corrector
import gender_predict


def main():
    database = None

    while True:
        option = int(input(
            "Choose option:\n 1 - correct data and create Email/password and predict gender\n 2 - add user\n 3 - Print database\n 4 - Exit\n"))


        if option == 1:
            data_corrector.correct_data()
            database = gender_predict.make_predict()

        elif option == 2:
            data_corrector.online_correct()
            database = gender_predict.make_predict()

        elif option == 3:
            print(database)

        if option == 4:
            break

if __name__ == "__main__":
    main()