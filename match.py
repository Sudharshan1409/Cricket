from innings import first_innings, second_innings, match_init


def match_start():
    # format = input("Enter the format of the match: ")
    # target = input("Enter the target: ")

    # if target == "":
    #     target = None
    # else:
    #     target = int(target)
    match = match_init("T20", 200)
    print("Match Started")
    if (match["innings"] == 1) and (match["target"] is None):
        first_innings(match)
    elif (match["innings"] == 2) and (match["target"] is not None):
        second_innings(match)


match_start()
