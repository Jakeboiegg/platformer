import json


def main():
    intro_text = """
    Hi. This is the data_recovery program for 'data.json'.
    This program will likely not recover your data, but will reset the file and format it.

    You are likely reading this for 3 reasons:

    1. You know what you are doing, go ahead.
       (open the file yourself, the program can't read the damaged file if thats what you are looking for)
    2. You are desparate to repair your file so that you can play the game, proceed with caution.
    3. You have no idea why you are here, please leave the program.

    You have 2 options:
    | reset | quit |
    """

    confirm_text = """


    Are you sure you want to delete your data?
    Type 'CONFIRM' to rewrite the 'data.json' file.
    Type anything else to quit.

    | CONFIRM | quit |
    """

    # main
    print(intro_text)
    option = input("    option: ")

    if option.lower() == "reset":
        print(confirm_text)
        option2 = input("    option: ")

        if option2 == "CONFIRM":
            reformat()
            print("    rewriten")

    print("    recovery program quit")


def reformat():
    reset_data = {
        "time_set": False,
        "minutes": 0,
        "seconds": 0,
        "milliseconds": 0,
        "frames_elapsed": 0,
    }
    with open("data.json", "w") as file:
        json.dump(reset_data, file)


if __name__ == "__main__":
    main()
